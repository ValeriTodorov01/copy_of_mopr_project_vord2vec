import unittest
import math
from main import distance, distance_to_hyperplane, K_D_Tree, sort_dict, Node

class TestKdTree(unittest.TestCase):

    def test_distance(self):
        p1 = [1, 2, 3]
        p2 = [4, 5, 6]
        result = distance(p1, p2)
        expected = math.sqrt((1-4)**2 + (2-5)**2 + (3-6)**2)
        self.assertEqual(result, expected)

    def test_sort_dict(self):
        dictionary = {'a': [3, 2, 1], 'b': [1, 2, 3], 'c': [2, 3, 1]}
        index = 1
        result = sort_dict(dictionary, index)
        expected = {'b': [1, 2, 3], 'c': [2, 3, 1], 'a': [3, 2, 1]}
        self.assertEqual(result, expected)

    def test_distance_to_hyperplane(self):
        given_point_coords = [1, 2, 3]
        plane_point_coords = [4, 5, 6]
        normal_vector = [0, 0, 1]
        result = distance_to_hyperplane(given_point_coords, plane_point_coords, normal_vector)
        expected = abs(3 - 6) / math.sqrt(1)
        self.assertEqual(result, expected)

    def test_insert_into_tree(self):
        kd_tree = K_D_Tree()
        root = Node('root', [1, 2, 3])
        node = Node('node', [4, 5, 6])
        depth = 0
        result = kd_tree.insert_into_tree(root, node, depth)
        self.assertEqual(result, node)

    def test_build_kd_tree(self):
        kd_tree = K_D_Tree()
        words = {'a': [3, 2, 1], 'b': [1, 2, 3], 'c': [2, 3, 1]}
        result = kd_tree.build_kd_tree(words)
        self.assertIsNotNone(result)

    def test_find_nearest_vector_recursion(self):
        kd_tree = K_D_Tree()
        root = Node('root', [1, 2, 3])
        given_point = Node('point', [4, 5, 6])
        result = kd_tree.find_nearest_vector_recursion(root, given_point)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()