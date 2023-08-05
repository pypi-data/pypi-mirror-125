"""
Nodes representing different elements of a Gherkin feature file.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import parse

from gherlint import utils


class Node(ABC):
    """
    Base class for all concrete node types.
    """

    def __init__(self, parent: Optional[Node], line: int, column: int):
        self.parent = parent
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line}, column={self.column})"

    def get_root(self) -> Node:
        """Get the root node, i.e. the topmost parent in the hierarchy."""
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Node:
        """Create a node instance from the dictionary returned by the gherkin parser."""


class Document(Node):
    """Represents the file itself"""

    def __init__(
        self,
        line: int,
        column: int,
        filename: str,
        feature: Optional[Feature],
        comments: List[str],
        parent=None,
    ):
        super().__init__(parent, line, column)
        self.filename = filename
        self.feature = feature
        self.comments = comments

    @property
    def children(self):
        return [self.feature]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Node = None) -> Document:
        feature_data = data.get("feature")
        instance = cls(
            line=0,
            column=0,
            filename=data["filename"],
            feature=None,
            comments=data["comments"],
        )
        if feature_data:
            instance.feature = Feature.from_dict(feature_data, parent=instance)
        return instance


class Feature(Node):
    """Represents a Feature in a file."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        tags: List[str],
        language: str,
        name: str,
        description: str,
        children: List[Union[Background, Scenario, ScenarioOutline]],
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.language = language
        self.name = name
        self.description = description
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Feature:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=data["tags"],
            language=data["language"],
            name=data["name"],
            description=data["description"],
            children=[],
        )
        for child in data["children"]:
            for keyword, child_data in child.items():
                if keyword == "scenario":
                    if child_data["keyword"] in utils.get_keyword_candidates(
                        "scenario"
                    ):
                        instance.children.append(
                            Scenario.from_dict(child_data, parent=instance)
                        )
                    else:
                        instance.children.append(
                            ScenarioOutline.from_dict(child_data, parent=instance)
                        )
                elif keyword == "background":
                    instance.children.append(
                        Background.from_dict(child_data, parent=instance)
                    )
        return instance


class Background(Node):
    """Represents a background of a feature."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        name: str,
        description: str,
        children: List[Step],
    ):
        super().__init__(parent, line, column)
        self.name = name
        self.description = description
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Background:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            name=data["name"],
            description=data["description"],
            children=[],
        )
        instance.children = [Step.from_dict(s, parent=instance) for s in data["steps"]]
        return instance


class Scenario(Node):
    """Represents a scenario of a feature."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        tags: List[str],
        name: str,
        description: str,
        examples: List[Examples],
        children: List[Step],
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.name = name
        self.description = description
        self.examples = examples
        self.children = children
        self.parameters = extract_parameters(name)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Scenario:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=data["tags"],
            name=data["name"],
            description=data["description"],
            examples=[],
            children=[],
        )
        instance.examples = [
            Examples.from_dict(d, parent=instance) for d in data["examples"]
        ]
        instance.children = [Step.from_dict(s, parent=instance) for s in data["steps"]]
        return instance


class ScenarioOutline(Scenario):
    """Represents a scenario outline of a feature"""


class Step(Node):
    def __init__(
        self, parent: Optional[Node], line: int, column: int, keyword: str, text: str
    ):
        super().__init__(parent, line, column)
        self.type = self._get_english_keyword(keyword)
        self.text = text
        self.parameters = extract_parameters(text)

    @staticmethod
    def _get_english_keyword(keyword: str) -> str:
        """Get the corresponding english step keyword in lowercase from input in any (supported) language."""
        if keyword.strip() == "*":
            return "*"
        english_keywords = ("given", "when", "then", "and", "but")
        for english_keyword in english_keywords:
            if keyword.lower() in [
                kw.lower() for kw in utils.get_keyword_candidates(english_keyword)
            ]:
                return english_keyword
        raise ValueError(f"Unable to look up english step keyword for {keyword}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Step:
        return cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            keyword=data["keyword"],
            text=data["text"],
        )


class Examples(Node):
    def __init__(
        self,
        parent: Optional[Node],
        line: int,
        column: int,
        tags: List[str],
        name: str,
        description: str,
        parameters: List[str],
        values: Dict[str, List[str]],
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.name = name
        self.description = description
        self.parameters = parameters
        self.values = values

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Examples:
        parameters: List[str] = [cell["value"] for cell in data["tableHeader"]["cells"]]
        values: Dict[str, List[str]] = {param: [] for param in parameters}
        for row in data["tableBody"]:
            for param, entry in zip(parameters, row["cells"]):
                values[param].append(entry["value"])
        return cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=data["tags"],
            name=data["name"],  # can this be filled?!
            description=data["description"],
            parameters=parameters,
            values=values,
        )


def extract_parameters(text: str) -> Tuple[str]:
    """Extract parameters from a string (e. g. a step text).
    'Parameters' are placeholders defined in the Examples section of a
    Scenario Outline and are delimited with ``< >``."""
    pattern = "<{}>"
    return tuple(match.fixed[0] for match in parse.findall(pattern, text))  # type: ignore
