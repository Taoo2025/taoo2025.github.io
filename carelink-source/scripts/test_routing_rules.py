import unittest
from routing_rules import *
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

class RoutingTests(unittest.TestCase):
    def test_direction_and_access(self):
        self.assertEqual(directions({'oneway':'-1'}),(False,True))
        self.assertEqual(directions({'junction':'roundabout'}),(True,False))
        self.assertEqual(directions({'highway':'motorway_link'}),(True,False))
        self.assertEqual(directions({'oneway':'yes','oneway:motorcar':'no'}),(True,True))
        self.assertFalse(access_allowed({'access':'private'}))
        self.assertTrue(access_allowed({'access':'no','motorcar':'yes'}))
        self.assertTrue(blocked_node({'barrier':'bollard'}))
        self.assertFalse(blocked_node({'barrier':'bollard','motorcar':'yes'}))
        self.assertAlmostEqual(speed_kmh('20 mph',60),32.18688)

    def test_prohibited_turn_changes_shortest_path(self):
        edges={(1,2):(1,1,10),(2,3):(1,1,20),(2,4):(2,2,30),(4,3):(2,2,30)}
        rules={2:[{'from':10,'to':20,'kind':'no_left_turn'}]}
        expanded=list(expand_turns(edges,rules));nodes=list({x for a,b,v in expanded for x in (a,b)});idx={x:i for i,x in enumerate(nodes)}
        g=csr_matrix(([v[0] for a,b,v in expanded],([idx[a] for a,b,v in expanded],[idx[b] for a,b,v in expanded])),shape=(len(nodes),len(nodes)))
        self.assertEqual(dijkstra(g,indices=idx[1])[idx[3]],5)
        self.assertFalse(turn_allowed(1,2,1,10,10,[{'from':10,'to':10,'kind':'no_u_turn'}]))
        self.assertTrue(turn_allowed(1,2,3,10,10,[{'from':10,'to':10,'kind':'no_u_turn'}]))
        self.assertFalse(turn_allowed(1,2,3,10,20,[{'from':10,'to':30,'kind':'only_right_turn'}]))

if __name__=='__main__':unittest.main()
