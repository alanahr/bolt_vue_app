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