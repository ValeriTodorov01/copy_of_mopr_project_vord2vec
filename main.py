import math


def distance(point_coords_1, point_coords_2):
    assert point_coords_1 is not None
    assert point_coords_2 is not None
    assert isinstance(point_coords_1, list)
    assert isinstance(point_coords_2, list)
    assert len(point_coords_1) == len(point_coords_2)

    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(point_coords_1, point_coords_2)))


def sort_dict(dictionary, index):
    assert dictionary is not None
    assert isinstance(dictionary, dict)
    assert isinstance(index, int)
    assert len(dictionary) > 0
    assert len(next(iter(dictionary.values()))) > index

    dictionary = sorted(dictionary.items(), key=lambda x: x[1][index])
    return dict(dictionary)


def distance_to_hyperplane(given_point_coords, plane_point_coords, normal_vector):
    assert given_point_coords is not None
    assert plane_point_coords is not None
    assert len(given_point_coords) == len(plane_point_coords) == len(normal_vector)
    assert len(given_point_coords) > 0

    dot_product = sum(
        (given_point_coords[i] - plane_point_coords[i]) * normal_vector[i] for i in range(len(given_point_coords)))
    magnitude_normal = math.sqrt(sum(component ** 2 for component in normal_vector))

    distance_between_point_and_hyperplane = abs(dot_product) / magnitude_normal
    return distance_between_point_and_hyperplane


class Node:
    def __init__(self, name, coords, left=None, right=None, has_not_been_used=True):
        assert name is not None
        assert coords is not None
        assert name != ""
        assert len(coords) > 0
        self.name = name
        self.coords = coords
        self.left = left
        self.right = right
        self.has_not_been_used = has_not_been_used


class K_D_Tree:
    def __init__(self):
        self.size = 0
        self.best_distance = -1

    def insert_into_tree(self, root, node, depth):
        assert node is not None

        if root is None:
            return node

        index = depth % len(node.coords)

        if node.coords[index] < root.coords[index]:
            root.left = node
        else:
            root.right = node

        return node

    def build_kd_tree(self, vectors, depth=0, root=None):
        assert vectors is not None
        assert isinstance(vectors, dict)

        if len(vectors) == 0:
            return None

        vectors = sort_dict(vectors, depth % len(list(vectors.values())[0]))

        mid = len(vectors) // 2
        if mid % 2 == 0:
            mid -= 1

        middle_node_name = list(vectors.keys())[mid]

        new_node = Node(middle_node_name, vectors[middle_node_name])
        root = self.insert_into_tree(root, new_node, depth - 1)

        if mid >= 0:
            left_dict = dict(list(vectors.items())[:mid])
            self.build_kd_tree(left_dict, depth + 1, root)

            right_dict = dict(list(vectors.items())[1 + mid:])
            self.build_kd_tree(right_dict, depth + 1, root)

        return root

    def find_nearest_vector_recursion(self, root, given_point, depth=0, best=None):
        if root is None:
            return None

        index = depth % len(given_point.coords)

        if best is None:
            best = root

        opposite_branch = None

        if self.best_distance == -1 and root.has_not_been_used:
            best = root
            self.best_distance = distance(given_point.coords, best.coords)

        else:
            probable_new_best_distance = distance(given_point.coords, root.coords)
            if self.best_distance > probable_new_best_distance and root.has_not_been_used:
                best = root
                self.best_distance = distance(given_point.coords, best.coords)

        if root.coords[index] > given_point.coords[index]:
            opposite_branch = root.right
            result_node = self.find_nearest_vector_recursion(root.left, given_point, depth + 1, best)

        else:
            opposite_branch = root.left
            result_node = self.find_nearest_vector_recursion(root.right, given_point, depth + 1, best)

        if result_node is not None and result_node.has_not_been_used:
            best = result_node

        if root is not None:
            normal_vector = [0] * len(given_point.coords)
            normal_vector[index] = 1
            distance_between_best_and_given = distance(given_point.coords, best.coords)
            if distance_between_best_and_given > distance_to_hyperplane(given_point.coords, root.coords, normal_vector):
                if self.best_distance == -1 or distance_between_best_and_given <= self.best_distance:
                    best_temp = self.find_nearest_vector_recursion(opposite_branch, given_point, depth, best)
                    if best_temp is not None and best.has_not_been_used:
                        best = best_temp
                    self.best_distance = distance(best.coords, given_point.coords)

        return best

    def find_nearest_vector(self, root, given_point):
        assert root is not None
        assert given_point is not None
        self.best_distance = -1
        return self.find_nearest_vector_recursion(root, given_point)

    def find_nearest_n_vectors(self, root, given_point, n):
        assert root is not None
        assert isinstance(root, Node)
        assert given_point is not None
        assert isinstance(given_point, Node)
        assert n > 0
        assert isinstance(n, int)

        nearest_vector = []
        for i in range(n):
            node_to_append = self.find_nearest_vector(root, given_point)
            assert node_to_append is not None
            node_to_append.has_not_been_used = False
            nearest_vector.append(node_to_append)

        for i in nearest_vector:
            i.has_not_been_used = True

        return nearest_vector

    def find_all_points_in_sphere(self, root, target_word, side):
        list_of_words_in_sphere = []
        found_words_counter = 0

        while True:
            potential_node = self.find_nearest_n_vectors(root, target_word, found_words_counter+1)
            if distance(potential_node[len(potential_node)-1].coords, target_word.coords) < side:
                list_of_words_in_sphere.append(potential_node[len(potential_node)-1])
                found_words_counter += 1

            else:
                return list_of_words_in_sphere
