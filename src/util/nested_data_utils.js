d && itemMap[item.parentId]) {
      // If item has a parent, add it to the parent's children array
      itemMap[item.parentId].children.push(node);
    } else {
      // If no parentId or parent not found, it's a root item
      nestedTree.push(node);
    }
  });

  return nestedTree;
}

// Example Usage:
const flatData = [
  { id: 1, name: 'Root 1', parentId: null },
  { id: 2, name: 'Child 1.1', parentId: 1 },
  { id: 3, name: 'Root 2', parentId: null },
  { id: 4, name: 'Child 1.1.1', parentId: 2 },
  { id: 5, name: 'Child 2.1', parentId: 3 },
];

const nestedData = flatToNested(flatData);
console.log(JSON.stringify(nestedData, null, 2));


 function flattenTree(nodes, flatArray = [], parentId = null) {
      nodes.forEach(node => {
        const newNode = { ...node }; // Create a copy to avoid modifying original
        newNode.parentId = parentId; // Add parentId to the flattened object
        delete newNode.children; // Remove children property from the flattened object
        flatArray.push(newNode);

        if (node.children && node.children.length > 0) {
          flattenTree(node.children, flatArray, node.id); // Assuming 'id' is the unique identifier
        }
      });
      return flatArray;
    }

    // Example usage:
    const nestedData = [
      { id: 1, name: 'Parent 1', children: [
        { id: 2, name: 'Child 1.1', children: [
          { id: 3, name: 'Grandchild 1.1.1' }
        ]},
        { id: 4, name: 'Child 1.2' }
      ]},
      { id: 5, name: 'Parent 2' }
    ];

    const flattenedData = flattenTree(nestedData);
    console.log(flattenedData);


function getAncestors(tree, targetId, parentPath = []) {
  // If the current node is an array, iterate over its elements.
  if (Array.isArray(tree)) {
    for (const node of tree) {
      const ancestors = getAncestors(node, targetId, parentPath);
      if (ancestors.length > 0) {
        return ancestors; // Found the target, return the path
      }
    }
  } 
  // If the current node is an object, check its properties.
  else if (typeof tree === 'object' && tree !== null) {
    // If the current node is the target, return the accumulated parent path.
    if (tree.id === targetId) {
      return [...parentPath, tree]; // Include the target itself in the ancestors
    }

    // Add the current node to the parent path for its children.
    const newParentPath = [...parentPath, tree];

    // Recursively search in 'children' property if it exists and is an array.
    if (tree.children && Array.isArray(tree.children)) {
      const ancestors = getAncestors(tree.children, targetId, newParentPath);
      if (ancestors.length > 0) {
        return ancestors;
      }
    }

    // You might need to extend this to other nested properties if your structure differs.
    // For example, if you have 'items' or other nested arrays/objects.
  }
  return []; // Target not found in this branch
}

// Example usage:
const data = {
  id: 1,
  name: "Root",
  children: [
    {
      id: 2,
      name: "Child A",
      children: [
        { id: 3, name: "Grandchild X" },
        { id: 4, name: "Grandchild Y" },
      ],
    },
    {
      id: 5,
      name: "Child B",
      children: [{ id: 6, name: "Grandchild Z" }],
    },
  ],
};

const targetId = 4;
const ancestors = getAncestors(data, targetId);
console.log(ancestors.map(node => node.name)); // Output: ["Root", "Child A", "Grandchild Y"]