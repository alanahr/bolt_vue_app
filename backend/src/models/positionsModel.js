import { v4 as uuidv4 } from 'uuid';

// In-memory storage (replace with database in production)
let positions = [
  {
    id: 1,
    name: 'Software Engineer',
    start_year: 2010,
    start_month: 1,
    start_day: 1,
    end_year: 2015,
    end_month: 3,
    end_day: 1,
    salary: 123456,
    details: [
      {
        id: 1,
        name: 'Participated in Agile Core engineering team in an Agile environment, participated in daily standup and planning, addressed bugs and stories, collaborated with others to solve problems, and advised junior colleagues',
        description: {
          type: 'doc',
          content: [
            {
              type: 'paragraph',
              content: [
                {
                  type: 'text',
                  text: 'This is still the text editor you\'re used to, but enriched with node views.',
                },
              ],
            },
          ],
        },
        tags: [],
        details: [
          {
            id: 2,
            name: "main job thing I'm talking about here like TestRail",
            tags: [],
            description: {},
            details: [],
          },
          {
            id: 3,
            name: 'Presentations and arcgis',
            tags: [],
            description: {
              type: 'doc',
              content: [
                {
                  type: 'heading',
                  attrs: { level: 1 },
                  content: [{ type: 'text', text: 'Lorem Ipsum' }],
                },
                {
                  type: 'paragraph',
                  content: [
                    {
                      type: 'text',
                      text: 'Justo laoreet sit amet cursus sit. In massa tempor nec feugiat nisl pretium fusce.',
                    },
                  ],
                },
              ],
            },
            details: [],
          },
        ],
      },
    ],
  },
];

let nextId = 2;

export const findAll = async () => {
  return positions;
};

export const findById = async (id) => {
  return positions.find(p => p.id === id);
};

export const create = async (positionData) => {
  const newPosition = {
    id: nextId++,
    ...positionData,
    details: positionData.details || [],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
  
  positions.push(newPosition);
  return newPosition;
};

export const update = async (id, positionData) => {
  const index = positions.findIndex(p => p.id === id);
  if (index === -1) return null;
  
  positions[index] = {
    ...positions[index],
    ...positionData,
    id, // Ensure ID doesn't change
    updated_at: new Date().toISOString(),
  };
  
  return positions[index];
};

export const remove = async (id) => {
  const index = positions.findIndex(p => p.id === id);
  if (index === -1) return false;
  
  positions.splice(index, 1);
  return true;
};