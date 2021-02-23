from operator import attrgetter
from math import sqrt


class Node:
    def __init__(self, parent, tile_index_position):
        self.g = 0  # start to node
        self.h = 0  # node to end
        self.f = 0  # start to end

        self.parent = parent
        self.xy = tile_index_position


class PathFinder:
    def __init__(self, room_map):
        self.map = room_map

    def find_path(self, startxy, endxy):  # params are tuple of entity position
        opened = []
        closed = []
        existing = {}  # use "x_y" as key
        tile_width, tile_height = self.map.tilewidth, self.map.tileheight
        map_width, map_height = self.map.width, self.map.height

        # create start and end node:
        start = Node(None, (int(startxy[0] / tile_width),
                            int(startxy[1] / tile_height)))
        end = Node(None, (int(endxy[0] / tile_width),
                          int(endxy[1] / tile_height)))
        existing[str(start.xy[0]) + "_" + str(start.xy[1])] = start
        existing[str(end.xy[0]) + "_" + str(end.xy[1])] = end
        opened.append(start)

        while opened:
            # create current node (sort by f then by h):
            current = min(opened, key=attrgetter('f', 'h'))
            opened.remove(current)
            closed.append(current)

            # make path:
            if current == end:
                path = []
                current_node = current
                while current_node is not None:
                    path.append(current_node.xy)
                    current_node = current_node.parent
                path = path[::-1]
                return path

            cur_x, cur_y = current.xy[0], current.xy[1]

            # for every adjacent tile:
            for adj_x in range(cur_x - 1, cur_x + 2):
                for adj_y in range(cur_y - 1, cur_y + 2):
                    if 0 <= adj_x < map_width and 0 <= adj_y < map_height:

                        # check if the node exists:
                        # noinspection PyUnusedLocal
                        adj = None
                        key = str(adj_x) + "_" + str(adj_y)
                        if key not in existing:
                            adj = Node(current, (adj_x, adj_y))
                            existing[key] = adj
                        else:
                            adj = existing.get(key)

                        # check if the node is walkable:
                        tile_info = self.map.get_tile_properties(
                            adj_x, adj_y, 0)
                        if tile_info['type'] == 'wall' or adj in closed:
                            continue

                        # check if diagonal jumps are valid:
                        if adj_x != cur_x and adj_y != cur_y:
                            tile1 = self.map.get_tile_properties(
                                cur_x, adj_y, 0)
                            tile2 = self.map.get_tile_properties(
                                adj_x, cur_y, 0)
                            if 'wall' in [tile1['type'], tile2['type']]:
                                continue

                        # update some parameters and lists:
                        extra_g = sqrt(abs(current.xy[0] - adj.xy[0]) ** 2 +
                                       abs(current.xy[1] - adj.xy[1]) ** 2)
                        new_g = current.g + extra_g
                        if new_g < adj.g or adj not in opened:
                            adj.g = new_g
                            adj.h = sqrt(abs(adj.xy[0] - end.xy[0]) ** 2 +
                                         abs(adj.xy[1] - end.xy[1]) ** 2)
                            adj.f = adj.g + adj.h
                            adj.parent = current

                            if adj not in opened:
                                opened.append(adj)

        # if no path:
        return None
