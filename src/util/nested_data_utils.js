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