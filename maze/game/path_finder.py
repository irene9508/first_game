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
    def __init__(self, map):
        self.map = map

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

                # skip unnecessary nodes:
                new_path = []
                checkpoint = path[0]
                new_path.append(checkpoint)
                for index in range(1, len(path) - 1):
                    walkable = self.check_if_walkable(checkpoint,
                                                      path[index + 1])
                    if not walkable:
                        checkpoint = path[index]
                        new_path.append(path[index])
                new_path.append(path[-1])
                return new_path

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
                            tile_info1 = self.map.get_tile_properties(
                                cur_x, adj_y, 0)
                            tile_info2 = self.map.get_tile_properties(
                                adj_x, cur_y, 0)
                            if 'wall' in [tile_info1['type'], tile_info2['type']]:
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

    def check_if_walkable(self, point1, point2):
        tile_width = self.map.tilewidth
        tile_height = self.map.tileheight
        p1 = (point1[0] * tile_width + tile_width / 2,
              point1[1] * tile_height + tile_height / 2)
        p2 = (point2[0] * tile_width + tile_width / 2,
              point2[1] * tile_height + tile_height / 2)
        vector1 = (p2[0] - p1[0], p2[1] - p1[1])
        length1 = sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
        v_norm1 = (vector1[0] / length1, vector1[1] / length1)

        for distance in range(0, int(length1), int(tile_width / 5)):
            x1 = p1[0] + v_norm1[0] * distance
            y1 = p1[1] + v_norm1[1] * distance

            tile_info1 = self.map.get_tile_properties(
                x1 / tile_width, y1 / tile_height, 0)
            tile_info2 = self.map.get_tile_properties(
                x1 / tile_width + 0.5, y1 / tile_height + 0.5, 0)
            tile_info3 = self.map.get_tile_properties(
                x1 / tile_width - 0.5, y1 / tile_height - 0.5, 0)

            if 'wall' in [tile_info1['type'], tile_info2['type'], tile_info3['type']]:
                return False

        # if no wall tile was found, return True:
        return True
