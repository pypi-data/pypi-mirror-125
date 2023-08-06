"""An extended version of SAM learner that is able to handle predicates inconsistency."""
from collections import defaultdict
from typing import Optional, Dict, Set, NoReturn, Iterable, List

from pddl.pddl import Action, Domain, Effect

from .core import ExtendedMatcher, extract_effects, ProxyActionGenerator
from .sam_learner import SAMLearner
from .sam_models import Mode, GroundedAction, State, ComparablePredicate


def sort_predicates(predicates: Iterable[ComparablePredicate]) -> List[ComparablePredicate]:
	"""Sorts the predicate list so that it could be compared to other lists.

	:param predicates: the predicates to sort.
	:return: the sorted predicate list.
	"""
	return sorted(
		predicates, key=lambda predicate: (predicate.name, str(predicate.signature)))


class ESAMLearner(SAMLearner):
	"""Extension to the SAM Learning algorithm."""

	matcher: ExtendedMatcher
	proxy_actions: Dict[str, List[Action]]
	proxy_action_generator: ProxyActionGenerator
	cannot_be_add_effects: Dict[str, Set[ComparablePredicate]]
	cannot_be_del_effects: Dict[str, Set[ComparablePredicate]]

	def __init__(
			self, working_directory_path: Optional[str] = None, domain_file_name: str = "domain.pddl",
			mode: Mode = "production", domain: Optional[Domain] = None, known_actions: Dict[str, Action] = {}):
		super().__init__(working_directory_path, domain_file_name, mode, domain, known_actions)
		self.cannot_be_add_effects = defaultdict(set)
		self.cannot_be_del_effects = defaultdict(set)
		self.proxy_action_generator = ProxyActionGenerator()
		self.proxy_actions = defaultdict(list)
		if mode == "development":
			self.matcher = ExtendedMatcher(domain=domain)
			return

		domain_path = self.working_directory_path / domain_file_name
		self.matcher = ExtendedMatcher(domain_path=str(domain_path))

	def add_new_action(
			self, grounded_action: GroundedAction, previous_state: State, next_state: State) -> NoReturn:
		"""

		:param grounded_action:
		:param previous_state:
		:param next_state:
		:return:
		"""
		if not self.proxy_action_generator.is_action_with_duplicated_parameters(grounded_action):
			super(ESAMLearner, self).add_new_action(grounded_action, previous_state, next_state)
			return

		new_proxy_action_name = self.proxy_action_generator.get_proxy_action_name(grounded_action)

	def update_action_effects(
			self, grounded_action: GroundedAction, previous_state: State, next_state: State) -> Effect:
		"""Updates the effects based on the fact that some fluents might need to be removed while others will be added.

		:param grounded_action: the action that is being observed in the trajectory component.
		:param previous_state: the state that the action was applied to.
		:param next_state: the new state created by applying the action on the previous state.
		:return: the effect created by removing impossible facts and adding new facts that were not observed.
		"""
		current_action: Action = self.learned_domain.actions[grounded_action.lifted_action_name]
		current_add_effects: Set = current_action.effect.addlist
		current_delete_effects: Set = current_action.effect.dellist
		grounded_add_effects, grounded_del_effects = extract_effects(previous_state, next_state)
		new_lifted_add_effects = set(self.matcher.get_possible_literal_matches(
			grounded_action, grounded_add_effects))
		new_lifted_delete_effects = set(self.matcher.get_possible_literal_matches(
			grounded_action, grounded_del_effects))

		if current_action.name in self.cannot_be_add_effects:
			self.logger.debug("removing the already removed add effects.")
			new_lifted_add_effects.difference_update(self.cannot_be_add_effects[current_action.name])

		if current_action.name in self.cannot_be_del_effects:
			self.logger.debug("removing the already removed delete effects.")
			new_lifted_delete_effects.difference_update(self.cannot_be_del_effects[current_action.name])

		consistent_add_effects = current_add_effects.intersection(new_lifted_add_effects)
		self.cannot_be_add_effects[current_action.name].update(current_add_effects.difference(new_lifted_add_effects))
		consistent_add_effects.update(new_lifted_add_effects.difference(current_add_effects))

		consistent_delete_effects = current_delete_effects.intersection(new_lifted_delete_effects)
		self.cannot_be_del_effects[current_action.name].update(
			current_delete_effects.difference(new_lifted_delete_effects))
		consistent_delete_effects.update(new_lifted_delete_effects.difference(current_delete_effects))

		action_effect = Effect()
		action_effect.addlist = set(sort_predicates(consistent_add_effects))
		action_effect.dellist = set(sort_predicates(consistent_delete_effects))
		return action_effect

	def update_action(
			self, grounded_action: GroundedAction, previous_state: State, next_state: State) -> NoReturn:
		"""Updates an action that was observed at least once already.

		:param grounded_action: the grounded action that was executed according to the trajectory.
		:param previous_state: the state that the action was executed on.
		:param next_state: the state that was created after executing the action on the previous
			state.
		"""
		action_name = grounded_action.lifted_action_name
		if self._is_known_action(action_name):
			return

		current_action: Action = self.learned_domain.actions[action_name]
		self._update_action_preconditions(current_action, grounded_action, previous_state)
		current_action.precondition = list(set(sort_predicates(current_action.precondition)))
		updated_effect = self.update_action_effects(grounded_action, previous_state, next_state)
		current_action.effect = updated_effect
		self.handle_maybe_effects(grounded_action, previous_state, next_state)
		self.logger.debug(f"Done updating the action - {grounded_action.lifted_action_name}")
