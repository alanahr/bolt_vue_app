function* findValuesByKey(obj, targetKey) {
  if (Array.isArray(obj)){
    obj.forEach(o => {
      yield* findValuesByKey(o, targetKey);
    })
  }
  if (typeof obj === 'object'){
    // Iterate over the object's properties
    for (const key in obj) {
      // Ensure the property belongs to the object itself, not its prototype chain
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const value = obj[key];
        // If the current key matches the targetKey, yield the value
        if (key === targetKey) {
          yield value;
        }
        // If the value is an object (and not null), recursively call the generator
        // and yield all values found in the nested object
        if (typeof value === 'object' && value !== null) {
          yield* findValuesByKey(value, targetKey);
        }
      }
    }
  }
}
// Example usage:
const nestedObject = {
  id: 1,
  name: 'Parent',
  details: {
    id: 2,
    description: 'Some details',
    nestedData: {
      id: 3,
      value: 'Deeply nested value'
    }
  },
  items: [
    { id: 4, name: 'Item A' },
    { id: 5, name: 'Item B' }
  ]
};
console.log('Finding all "id" values:');
for (const idValue of findValuesByKey(nestedObject, 'id')) {
  console.log(idValue);
}

//todo test - seems wrong
function flattenEntityTree(nodes, flatArray = [], entity_parent_id = null) {
  nodes.forEach(node => {
    const newNode = { ...node }; // Create a copy to avoid modifying original
    newNode.entity_parent = entity_parent_id; // Add parentId to the flattened object
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
const flattenedData = flattenEntityTree(nestedData);
console.log(flattenedData);


//todo not used
function flatToNestedViaEntityParent(data) {
  const result = [];
  const itemMap = {};

  data.forEach(item => {
    itemMap[item.id] = item; // Store reference

    if (item.entity_parent) {
      const parent = itemMap[item.entity_parent];
      if (parent) {
        if (!parent.children) {
          parent.children = [];
        }
        parent.children.push(item);
      }
    } else {
      result.push(item); // Top-level item
    }
  });

  return result;
}
// Example Usage:
const flatData = [
  { id: 1, name: 'Root 1', parentId: null },
  { id: 2, name: 'Child 1.1', parentId: 1 },
  { id: 3, name: 'Root 2', parentId: null },
  { id: 4, name: 'Child 1.1.1', parentId: 2 },
  { id: 5, name: 'Child 2.1', parentId: 3 },
];
const nestedData = flatToNestedViaEntityParent(flatData);
console.log(JSON.stringify(nestedData, null, 2));


// use this one
function flatToNestedEntity(flatArray) {
  const itemMap = {}; // Map to store items by their ID for quick lookup
  const nestedTree = []; // Array to store root-level items

  // Step 1 & 2: Create map and initialize children arrays
  flatArray.forEach(item => {
    itemMap[item.id] = { ...item, children: [] }; // Deep copy and add children array
  });

  // Step 3: Build the tree
  flatArray.forEach(item => {
    const node = itemMap[item.id];
    if (item.entity_parent){ 
      if (typeof item.entity_parent == "object" && itemMap[item.entity_parent.id]) {
        // If item has a parent, add it to the parent's children array
        itemMap[item.entity_parent.id].children.push(node);
      } else {
        itemMap[item.entity_parent].children.push(node);
      }
    } else {
       // If no parentId or parent not found, it's a root item
       nestedTree.push(node); 
    }
    });
  return nestedTree;
}
const nestedDatav2 = flatToNestedEntity(flatData);
console.log(JSON.stringify(nestedData, null, 2));


function getEntityAncestors(data, targetId, parentKey = 'parentId', idKey = 'id', ancestors = []) {
  for (const node of data) {
    if (node[idKey] === targetId) {
      return ancestors; // Target found, return collected ancestors
    }

    if (node.children && node.children.length > 0) {
      const result = getAncestors(node.children, targetId, parentKey, idKey, [...ancestors, node]);
      if (result) {
        return result; // Target found in a child branch
      }
    }
  }
  return null; // Target not found in this branch
}

//#todo - make yield function/generator
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
// Example Usage:
const treeData = [
  { id: 1, name: 'Node A', children: [
    { id: 2, name: 'Node B', parentId: 1, children: [
      { id: 3, name: 'Node C', parentId: 2 },
      { id: 4, name: 'Node D', parentId: 2 }
    ]},
    { id: 5, name: 'Node E', parentId: 1 }
  ]},
  { id: 6, name: 'Node F' }
];
const targetNodeId = 3;
const ancestors = getAncestors(treeData, targetNodeId);
if (ancestors) {
  console.log(`Ancestors of node ${targetNodeId}:`, ancestors.map(node => node.name));
} else {
  console.log(`Node ${targetNodeId} not found.`);



