from pprint import pprint

from typing import List, Tuple, Dict

from conftest import service2l


def refine_entry(entry: Tuple[str]) -> List[str]:
    """
    Remove prefix and parameters from entry.
    """
    verb, path = entry
    path_parts = path.lstrip('/api/v1/').split('/')
    path_parts = [x for x in path_parts if not x.startswith('{')]
    return [verb, *path_parts]


def dedupe(endpoints: List[str]) -> List[str]:
    """
    Remove duplicates and enclosing endpoints.
    """
    paths_set = set([tuple(x) for x in endpoints])
    deduped_paths = []
    for path in paths_set:
        for other_path in paths_set:
            if path != other_path and path == other_path[:len(path)]:
                break
        else:
            deduped_paths.append(list(path))
    return deduped_paths



def build_tree(endpoints: List[str]) -> Dict:
    """
    Build tree out of the endpoints.
    """
    nested_dict = {}
    for endpoint in endpoints:
        current_dict = nested_dict
        for part in endpoint[1:-1]:
            current_dict = current_dict.setdefault(part, {})
        current_dict[endpoint[-1]] = endpoint[0]
    return nested_dict


if __name__ == '__main__':
    refined_endpoints = [refine_entry(x) for x in service2l]
    for e in refined_endpoints:
        print(e)
    print('z' * 80)
    deduped = sorted(dedupe(refined_endpoints))
    # for d in deduped:
    #     print(d)
    # print('x' * 80)
    tree = build_tree(deduped)
    pprint(tree)