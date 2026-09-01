from __future__ import annotations

from collections import defaultdict, deque

from .models import Asset


class AssetGraph:
    def __init__(self, assets: list[Asset]) -> None:
        self.assets = {item.id: item for item in assets}
        self.reverse: dict[str, set[str]] = defaultdict(set)
        for asset in assets:
            for dependency in asset.dependencies:
                if dependency not in self.assets:
                    raise ValueError(f"{asset.id} references missing asset {dependency}")
                self.reverse[dependency].add(asset.id)
        self._validate_cycle()

    def _validate_cycle(self) -> None:
        indegree = {key: len(item.dependencies) for key, item in self.assets.items()}
        queue = deque(sorted(key for key, count in indegree.items() if count == 0))
        visited = 0
        while queue:
            node = queue.popleft()
            visited += 1
            for dependent in self.reverse[node]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        if visited != len(self.assets):
            raise ValueError("asset dependency graph contains a cycle")

    def waves(self) -> list[list[str]]:
        remaining = set(self.assets)
        completed: set[str] = set()
        waves: list[list[str]] = []
        while remaining:
            ready = sorted(node for node in remaining if set(self.assets[node].dependencies).issubset(completed))
            if not ready:
                raise ValueError("no executable dependency wave")
            waves.append(ready)
            completed.update(ready)
            remaining.difference_update(ready)
        return waves

    def blast_radius(self, asset_id: str) -> int:
        queue = deque([asset_id])
        seen: set[str] = set()
        while queue:
            current = queue.popleft()
            for dependent in self.reverse[current]:
                if dependent not in seen:
                    seen.add(dependent)
                    queue.append(dependent)
        return len(seen)

