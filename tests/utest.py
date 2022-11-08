import unittest
from nontree.TreeMap import TreeMap
from nontree.NonTree import NonTree
from nontree.QuadTree import QuadTree
from nontree.BiTree import BiTree

# x = random.randrange(11, 29989)
# y = random.randrange(11, 19989)
POINTS = [(6808, 1972), (10684, 821), (20765, 5068), (10420, 8465), (6037, 10794), (2217, 19587), (29675, 3716),
          (14204, 14030), (11081, 17425), (5166, 10218), (28979, 13543), (23853, 14567), (7174, 13116), (3753, 4676),
          (16307, 13045), (2057, 6754), (1148, 12463), (18692, 11752), (5082, 10498), (1167, 12400), (23750, 2828),
          (14803, 12383), (9343, 13548), (18923, 10857), (27743, 19913), (5509, 17971), (5954, 15982), (25535, 16230),
          (15338, 1826), (11148, 13142), (22844, 5211), (20535, 14571), (4474, 12521), (2900, 5725), (5019, 5531),
          (4656, 8130), (24523, 18828), (28758, 14193), (22517, 16167), (8629, 4299), (9449, 11645), (10812, 4463),
          (28221, 16342), (21012, 1203), (19841, 19105), (9954, 16719), (11064, 686), (29811, 2551), (2835, 5422),
          (26929, 17659), (4110, 1726), (5834, 15599), (23543, 17328), (15193, 14606), (3611, 1428), (8176, 13087),
          (3184, 8576), (9917, 14155), (11629, 5660), (26717, 8600), (15906, 15723), (12126, 16951), (23072, 11253),
          (657, 5934), (19753, 12070), (23006, 17662), (25338, 16954), (16607, 17226), (16090, 19332), (28921, 4998),
          (6380, 7311), (23706, 9634), (16335, 9872), (18483, 14504), (7817, 17269), (21268, 2366), (29535, 2075),
          (5591, 3859), (15685, 7496), (28382, 11170), (26827, 10444), (17501, 320), (11664, 10973), (13972, 8580),
          (7381, 15625), (25961, 1644), (1071, 2188), (3314, 18864), (27037, 13121), (25773, 8609), (17740, 1993),
          (16135, 13157), (12783, 5902), (2368, 4401), (27713, 13116), (1798, 9439), (7295, 15004), (11490, 15281),
          (21394, 12747), (24296, 9545), (26492, 13069), (25020, 14201), (25526, 10544), (16572, 14913), (5358, 15782),
          (24596, 17979), (15052, 14936), (6711, 17180), (26171, 13652), (9093, 13328), (17807, 3090), (6879, 7668),
          (11677, 10279), (16360, 469), (22092, 5200), (29526, 9774), (22922, 12053), (660, 1529), (27901, 2088),
          (8366, 15801), (24639, 18774), (7295, 7820), (15557, 9835), (23065, 6589), (6576, 4055), (17311, 6887),
          (12836, 6384), (22681, 5764), (22997, 4217), (8212, 17771), (6979, 11874), (18568, 15477), (27236, 3238),
          (9084, 4835), (23907, 18550), (22159, 14235), (6138, 7078), (22377, 11366), (11264, 8217), (21470, 1198),
          (4801, 12171), (19101, 676), (1086, 14595), (9736, 15569), (24420, 12590), (19608, 9473), (5477, 12625),
          (6190, 16643), (11496, 1575), (2485, 2072), (8218, 10243), (19367, 13508), (26067, 14738), (2614, 19484),
          (14425, 18706), (17831, 17147), (11390, 2833), (21791, 11585), (18976, 4744), (25276, 18710), (13710, 8419),
          (9144, 4421), (5010, 3922), (29742, 2557), (18413, 4084), (27157, 19853), (22012, 10483), (13402, 1749),
          (10232, 15179), (25174, 1471), (1296, 12705), (730, 14130), (412, 15593), (12760, 8986), (15859, 682),
          (1230, 9442), (3910, 10635), (1118, 7038), (16555, 17100), (21205, 16009), (24347, 13559), (24375, 13916),
          (795, 16619), (3909, 12913), (18569, 277), (12373, 12836), (891, 4728), (11431, 16725), (21090, 9378),
          (22096, 10275), (10810, 2686), (12495, 7309), (26021, 8348), (23316, 19311), (4050, 7626), (28293, 19358),
          (18225, 3133), (23631, 4569), (9252, 17926), (12555, 7108), (28752, 3626), (25031, 14201), (8488, 3656),
          (15023, 11372), (15037, 9901), (13276, 502), (16329, 9580), (8062, 8220), (9462, 11589), (24902, 5892),
          (3974, 5256), (5081, 14364), (2780, 15951), (8649, 1626), (10589, 9875), (8899, 10696), (18679, 11900),
          (1030, 7136), (18549, 8402), (4435, 9927), (26224, 12553), (27735, 3132), (8299, 13761), (20269, 1020),
          (3605, 7068), (19337, 16212), (27575, 6439), (23377, 6384), (23363, 12256), (23686, 2645), (5147, 224),
          (12106, 15222), (8279, 10307), (1128, 4284), (10385, 1711), (12142, 19528), (24061, 5346), (23480, 10587),
          (26201, 5243), (11947, 15130), (23883, 19386), (4839, 4716), (3772, 18385), (317, 15556), (20380, 17658),
          (26929, 14373), (5199, 16502), (5748, 14285), (12946, 3019), (18706, 10882), (13501, 7884), (28801, 16474),
          (1849, 13542), (24436, 9264), (2001, 1170), (13744, 13343), (12407, 17402), (7330, 13048), (21407, 13674),
          (24883, 6792), (25186, 15300), (8279, 5702), (18426, 7725), (24599, 10169), (17319, 4667), (11032, 12954),
          (27107, 12559), (12027, 4136), (24133, 6038), (2518, 8214), (29986, 15542), (13373, 18527), (25631, 1393)]


class TreeMapPointTestCase(unittest.TestCase):
    def setUp(self):
        self.tm = TreeMap((0, 0, 3000, 2000))

    def test_add_test_point(self):
        self.tm.add((370, 270), "foo")
        ret = self.tm.test_point((370, 270))
        self.assertTrue(ret)
        ret = self.tm.test_point((370, 271))
        self.assertFalse(ret)

    def test_add_get_point(self):
        self.tm.add((370, 270), "foo")
        ret = self.tm.get_point((370, 270))
        self.assertEqual(ret, ["foo"])
        self.tm.add((370, 270), "bar")
        ret = self.tm.get_point((370, 270))
        self.assertEqual(ret, ["foo", "bar"])

    def test_add_del_point_test_point(self):
        self.tm.add((370, 270), "foo")
        self.tm.del_point((370, 270))
        ret = self.tm.test_point((370, 270))
        self.assertFalse(ret)

    def test_add_pop_point_test_point(self):
        self.tm.add((370, 270), "foo")
        ret = self.tm.pop_point((370, 270))
        self.assertEqual(ret, ["foo"])
        ret = self.tm.test_point((370, 270))
        self.assertFalse(ret)

    def test_add_discard_get_point(self):
        self.tm.add((370, 270), "foo")
        self.tm.add((370, 270), "bar")
        self.tm.discard((370, 270), "foo")
        ret = self.tm.get_point((370, 270))
        self.assertEqual(ret, ["bar"])

    def tearDown(self):
        pass


class TreeMapRectCircleTestCase(unittest.TestCase):
    def setUp(self):
        self.tm = TreeMap((0, 0, 20000, 30000))

        for x, y in POINTS:
            self.tm.add((x, y), "foo")

        self.tm.add((5555, 4444), "foo")

        self.tm.add((4, 4), "bar")
        self.tm.add((29999, 19999), "bar")

    def test_get_rect(self):
        ret = self.tm.get_rect((15, 15, 25000, 15000))
        self.assertIn("foo", ret)
        self.assertNotIn("bar", ret)

    def test_get_circle(self):
        ret = self.tm.get_circle((15000, 10000, 9900))
        self.assertIn("foo", ret)
        self.assertNotIn("bar", ret)

    def test_get_rect_zero(self):
        ret = self.tm.get_rect((30000, 20000, 1, 1))
        self.assertEqual(len(ret), 0)

    def test_get_circle_zero(self):
        ret = self.tm.get_circle((30000, 20000, 1))
        self.assertEqual(len(ret), 0)

    def test_test_rect(self):
        ret = self.tm.test_rect((15, 15, 25000, 15000))
        self.assertTrue(ret)
        ret = self.tm.test_rect((0, 0, 2, 2))
        self.assertFalse(ret)

    def test_test_circle(self):
        ret = self.tm.test_circle((5554, 4443, 77))
        self.assertTrue(ret)
        ret = self.tm.test_circle((0, 0, 2))
        self.assertFalse(ret)

    def test_del_rect_test_rect(self):
        self.tm.del_rect((15, 15, 25000, 15000))
        ret = self.tm.test_rect((15, 15, 25000, 15000))
        self.assertFalse(ret)

    def test_del_circle_test_circle(self):
        self.tm.del_circle((5554, 4443, 77))
        ret = self.tm.test_circle((5554, 4443, 77))
        self.assertFalse(ret)

    def tearDown(self):
        pass


class TreeMapGeneralTestCase(unittest.TestCase):
    def setUp(self):
        self.tm = TreeMap((0, 0, 20000, 30000))

        for x, y in POINTS:
            self.tm.add((x, y), "foo")

    def test_copy_datapoints_data(self):
        cpy = self.tm.copy()
        ret = [dp for dp in self.tm.datapoints()]
        retcpy = [dp for dp in cpy.datapoints()]
        self.assertEqual(ret, retcpy)
        ret = [dp for dp in self.tm.data()]
        retcpy = [dp for dp in cpy.data()]
        self.assertEqual(ret, retcpy)

    def test_repr_datapoints_data(self):
        cpy = eval(repr(self.tm))
        ret = [dp for dp in self.tm.datapoints()]
        retcpy = [dp for dp in cpy.datapoints()]
        self.assertEqual(ret, retcpy)
        ret = [dp for dp in self.tm.data()]
        retcpy = [dp for dp in cpy.data()]
        self.assertEqual(ret, retcpy)

    def test_discard_datapoints_datapoints(self):
        self.tm.discard_datapoints([((6808, 1972), "foo"), ((10684, 821), "foo")])
        ret = [dp for dp in self.tm.datapoints()]
        self.assertNotIn(((6808, 1972), "foo"), ret)
        self.assertNotIn(((10684, 821), "foo"), ret)

    def test_add_datapoints_datapoints(self):
        self.tm.add_datapoints([((1, 1), "foo"), ((2, 2), "bar")])
        ret = [dp for dp in self.tm.datapoints()]
        self.assertIn(((1, 1), "foo"), ret)
        self.assertIn(((2, 2), "bar"), ret)

    def test_clear_prune(self):
        self.tm.clear()
        self.assertEqual(len(self.tm), 0)
        self.tm.prune()
        self.assertIsNone(self.tm.root.subtrees)

    def tearDown(self):
        pass


class NonTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.nt = NonTree((0, 0, 3000, 2000))

    def test_add_test_point(self):
        self.nt.add((17, 37))
        ret = self.nt.test_point((17, 37))
        self.assertTrue(ret)
        ret = self.nt.test_point((17, 38))
        self.assertFalse(ret)

    def test_add_get_point(self):
        self.nt.add((17, 37))
        ret = self.nt.get_point((17, 37))
        self.assertEqual(ret, [(17, 37)])
        ret = self.nt.get_point((17, 38))
        self.assertEqual(ret, [])

    def test_add_get_encompassed(self):
        for p in POINTS:
            self.nt.add(p)
        ret = self.nt.get_encompassed()
        self.assertEqual(ret.sort(), POINTS.sort())

    def tearDown(self):
        pass


class NonTreeStaticTestCase(unittest.TestCase):
    def test_encompass_rectrect(self):
        ret = NonTree.encompass_rectrect((1, 1, 7, 7), (2, 2, 4, 4))
        self.assertTrue(ret)
        ret = NonTree.encompass_rectrect((2, 2, 4, 4), (1, 1, 7, 7))
        self.assertFalse(ret)

    def test_collide_rectpoint(self):
        ret = NonTree.collide_rectpoint((0, 0, 100, 100), (60, 70))
        self.assertTrue(ret)
        ret = NonTree.collide_rectpoint((0, 0, 100, 100), (600, 700))
        self.assertFalse(ret)

    def test_collide_rectrect(self):
        ret = NonTree.collide_rectrect((0, 0, 100, 100), (50, 50, 100, 100))
        self.assertTrue(ret)
        ret = NonTree.collide_rectrect((0, 0, 100, 100), (101, 101, 2, 2))
        self.assertFalse(ret)

    def test_encompass_circlerect(self):
        ret = NonTree.encompass_circlerect((50, 50, 10), (48, 48, 4, 4))
        self.assertTrue(ret)
        ret = NonTree.encompass_circlerect((50, 50, 10), (0, 0, 100, 100))
        self.assertFalse(ret)

    def test_collide_rectcircle(self):
        ret = NonTree.collide_rectcircle((0, 0, 100, 100), (50, 50, 10))
        self.assertTrue(ret)
        ret = NonTree.collide_rectcircle((0, 0, 100, 100), (150, 150, 10))
        self.assertFalse(ret)

    def test_collide_circlepoint(self):
        ret = NonTree.collide_circlepoint((50, 50, 10), (51, 51))
        self.assertTrue(ret)
        ret = NonTree.collide_circlepoint((50, 50, 10), (510, 510))
        self.assertFalse(ret)


class QuadTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.nt = QuadTree((0, 0, 3000, 2000))

    def test_add_test_point(self):
        self.nt.add((17, 37))
        ret = self.nt.test_point((17, 37))
        self.assertTrue(ret)
        ret = self.nt.test_point((17, 38))
        self.assertFalse(ret)

    def test_add_get_point(self):
        self.nt.add((17, 37))
        ret = self.nt.get_point((17, 37))
        self.assertEqual(ret, [(17, 37)])
        ret = self.nt.get_point((17, 38))
        self.assertEqual(ret, [])

    def test_add_get_encompassed(self):
        for p in POINTS:
            self.nt.add(p)
        ret = self.nt.get_encompassed()
        self.assertEqual(ret.sort(), POINTS.sort())

    def tearDown(self):
        pass


class BiTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.nt = BiTree((0, 0, 3000, 2000))

    def test_add_test_point(self):
        self.nt.add((17, 37))
        ret = self.nt.test_point((17, 37))
        self.assertTrue(ret)
        ret = self.nt.test_point((17, 38))
        self.assertFalse(ret)

    def test_add_get_point(self):
        self.nt.add((17, 37))
        ret = self.nt.get_point((17, 37))
        self.assertEqual(ret, [(17, 37)])
        ret = self.nt.get_point((17, 38))
        self.assertEqual(ret, [])

    def test_add_get_encompassed(self):
        for p in POINTS:
            self.nt.add(p)
        ret = self.nt.get_encompassed()
        self.assertEqual(ret.sort(), POINTS.sort())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
