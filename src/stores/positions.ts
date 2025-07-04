import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Position } from '../types';
import type { Detail } from '../types';

export const usePositionStore = defineStore('positions', () => {
  const positions = ref<Position[]>([]);

  let nextId = 1;
  let nextDetailsId = 1;

  //initialize sample details for the position
  const details = {
    id: nextDetailsId++,
    name: 'Participated in Agile Core engineering team in an Agile environment, participated in daily standup and planning, addressed bugs and stories, collaborated with others to solve problems, and advised junior colleagues',
    description: {
      type: 'doc',
      from: 0,
      to: 159,
      content: [
        {
          type: 'paragraph',
          from: 0,
          to: 77,
          content: [
            {
              type: 'text',
              from: 1,
              to: 76,
              text: 'This is still the text editor you’re used to, but enriched with node views.',
            },
          ],
        },
        {
          type: 'vueComponent',
          from: 77,
          to: 78,
          attrs: {
            count: 0,
          },
        },
        {
          type: 'paragraph',
          from: 78,
          to: 157,
          content: [
            {
              type: 'text',
              from: 79,
              to: 156,
              text: 'Did you see that? That’s a Vue component. We are really living in the future.',
            },
          ],
        },
      ],
    },
    tags: [],

    details: [
      {
        id: nextDetailsId++,
        name: "main job thing I'm talking about here like TestRail",
        tags: [],
        description: {},
        details: [],
      },
      {
        id: nextDetailsId++,
        name: 'Presentations and arcgis',

        tags: [
        ],
        description: {
          type: 'doc',
          from: 0,
          to: 277,
          content: [
            {
              type: 'heading',
              from: 0,
              to: 13,
              attrs: {
                level: 1,
              },
              content: [
                {
                  type: 'text',
                  from: 1,
                  to: 12,
                  text: 'Lorem Ipsum',
                },
              ],
            },
            {
              type: 'paragraph',
              from: 13,
              to: 242,
              content: [
                {
                  type: 'text',
                  from: 14,
                  to: 241,
                  text: 'Justo laoreet sit amet cursus sit. In massa tempor nec feugiat nisl pretium fusce. Vel quam elementum pulvinar etiam non. Nisl nisi scelerisque eu ultrices vitae. Odio ut enim blandit volutpat maecenas volutpat blandit aliquam.',
                },
              ],
            },
            {
              type: 'bulletList',
              from: 242,
              to: 267,
              content: [
                {
                  type: 'listItem',
                  from: 243,
                  to: 266,
                  content: [
                    {
                      type: 'paragraph',
                      from: 244,
                      to: 265,
                      content: [
                        {
                          type: 'text',
                          from: 245,
                          to: 264,
                          text: 'this is a list item',
                        },
                      ],
                    },
                  ],
                },
              ],
            },
            {
              type: 'heading',
              from: 267,
              to: 271,
              attrs: {
                level: 2,
              },
              content: [
                {
                  type: 'text',
                  from: 268,
                  to: 270,
                  text: 'h2',
                },
              ],
            },
            {
              type: 'paragraph',
              from: 271,
              to: 273,
            },
            {
              type: 'paragraph',
              from: 273,
              to: 275,
            },
          ],
        },
      },
    ],
  };
  // Initialize with sample data
  const sampleData = [
    {
      id: nextId++,
      name: 'Software Engineer',
      start_year: 2010,
      start_month: 1,
      start_day: 1,
      end_year: 2015,
      end_month: 3,
      end_day: 1,
      salary: 123456,
      details: [details],
    },
  ];
  positions.value = sampleData;

  function addPosition(position: Omit<Position, 'id'>) {
    const newPosition = { ...position, id: nextId++, details: [] };
    positions.value.push(newPosition);
    return newPosition;
  }

  function updatePosition(id: number, position: Partial<Position>) {
    const index = positions.value.findIndex((p) => p.id === id);
    if (index !== -1) {
      positions.value[index] = { ...positions.value[index], ...position };
      return positions.value[index];
    }
    return null;
  }

  function deletePosition(id: number) {
    const index = positions.value.findIndex((p) => p.id === id);
    if (index !== -1) {
      positions.value.splice(index, 1);
      return true;
    }
    return false;
  }

  function getPosition(id: number) {
    return positions.value.find((p) => p.id === id);
  }

  function getPositions() {
    return positions.value;
  }

  return {
    positions,
    addPosition,
    updatePosition,
    deletePosition,
    getPosition,
    getPositions,
  };
});
