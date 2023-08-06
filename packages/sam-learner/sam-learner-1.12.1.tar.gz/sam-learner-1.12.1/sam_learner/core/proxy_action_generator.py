"""Generates proxy actions for the ESAM algorithm."""
from collections import defaultdict

from pddl.pddl import Action

from sam_learner.core.extended_predicate_matcher import contains_duplicates
from sam_learner.sam_models import GroundedAction


class ProxyActionGenerator:
    """Class that is able to know whether an action contains duplicates and can create a proxy action to represent
    the inconsistent action usage."""

    def is_action_with_duplicated_parameters(self, grounded_action: GroundedAction) -> bool:
        """An indicator on whether or not the grounded action contains duplicate objects in the signature.

        :param grounded_action: the grounded action that is currently being executed.
        :return: whether or not the action's signature has duplications.
        """
        grounded_action_objects = [signature_item[0] for signature_item in grounded_action.grounded_signature]
        return contains_duplicates(grounded_action_objects)

    def get_proxy_action_name(self, grounded_action: GroundedAction) -> str:
        """Get the name of the proxy action that represents the action with the duplicate parameters.

        :param grounded_action: the grounded action that contains duplicate objects in its signature.
        :return: the name of the proxy action that is represented by the duplicated objects.
        """
        grounded_objects = [signature_item[0] for signature_item in grounded_action.grounded_signature]
        objects_count = defaultdict(int)
        for object_name in grounded_objects:
            objects_count[object_name] += 1

        duplicate_objects = [object_name for object_name, count in objects_count.items() if count > 1]

        return f"{grounded_action.lifted_action_name}-duplicate-{'-'.join(duplicate_objects)}"

    def create_proxy_action(self, grounded_action: GroundedAction) -> Action:
        pass


