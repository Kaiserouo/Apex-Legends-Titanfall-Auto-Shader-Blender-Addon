+ Make node adder support shared node group
  + For the current implementation of node adders, they will create a brand new (effectively single user) node group
  + Should do this instead
    + group.node_tree = bpy.data.node_groups['OldNodeGroupName']
    + ref. https://blender.stackexchange.com/questions/23970/how-to-add-a-group-into-a-node-tree-with-python
+ Support multiple emission value changing
  + by making a shared value group that has a value node (emission strength) & emission texture multiply mix node inside (for changing color)
  + make node adder support fetching node group name? (also should set node group name! otherwise the node group (node) actually has empty label)