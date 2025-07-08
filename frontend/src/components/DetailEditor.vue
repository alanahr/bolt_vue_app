<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import Details from '@tiptap/extension-details';
import DetailsContent from '@tiptap/extension-details-content';
import DetailsSummary from '@tiptap/extension-details-summary';
import StarterKit from '@tiptap/starter-kit';
  
import type { Detail } from '../types/detail';
import type { Entity } from '../types/entity';
import { useEntityStore } from '../stores/entities';
import { VueDraggableNext } from 'vue-draggable-next';

//#TODO - add extensions for tiptap - https://next.tiptap.dev/docs/editor/extensions/nodes/details

const props = defineProps<{
  detail: Detail;
  level?: number;
}>();

const emit = defineEmits<{
  (e: 'update:detail', value: Detail): void;
}>();

const entityStore = useEntityStore();
const entities = ref<Entity[]>([]);
const searchQuery = ref('');
const selectedHeading = ref(1);
const showTagSearch = ref(false);

const editor = useEditor({
  content: props.detail.description || '',
  extensions: [
    StarterKit,
    Details.configure({
      persist: true,
      HTMLAttributes: {
        class: 'details',
      },
    }),
    DetailsSummary,
    DetailsContent,
  ],
  editorProps: {
    attributes: {
      class: 'form-control',
    },
  },
  onUpdate: ({ editor }) => {
    const updatedDetail = { ...props.detail };
    updatedDetail.description = editor.getJSON();
    emit('update:detail', updatedDetail);
  },
});

onMounted(() => {
  entities.value = entityStore.getEntities();
});

const changeHeading = (h: number) => {
  selectedHeading.value = h;
};

  
const checkHeadingL = computed(() => {
  if (editor.isActive('heading', { level: 1 })) {
    return 6;
  } else if (editor.isActive('heading', { level: 2 })) {
    return 1;
  } else if (editor.isActive('heading', { level: 3 })) {
    return 2;
  } else if (editor.isActive('heading', { level: 4 })) {
    return 3;
  } else if (editor.isActive('heading', { level: 5 })) {
    return 4;
  } else if (editor.isActive('heading', { level: 6 })) {
    return 5;
  }
});
const filteredEntities = computed(() => {
  return entities.value.filter(
    (entity) =>
      entity.name.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
      !props.detail.tags.some((tag) => tag.id === entity.id)
  );
});

const addTag = (entity: Entity) => {
  const updatedDetail = { ...props.detail };
  updatedDetail.tags.push(entity);
  emit('update:detail', updatedDetail);
  showTagSearch.value = false;
  searchQuery.value = '';
};

const removeTag = (tagId: number) => {
  const updatedDetail = { ...props.detail };
  updatedDetail.tags = updatedDetail.tags.filter((tag) => tag.id !== tagId);
  emit('update:detail', updatedDetail);
};

//#TODO should be date?? or uuid??
const addNestedDetail = () => {
  const updatedDetail = { ...props.detail };
  const newDetail: Detail = {
    id: Date.now(),
    name: '',
    description: {},
    tags: [],
    details: [],
  };
  updatedDetail.details.push(newDetail);
  emit('update:detail', updatedDetail);
};

const updateNestedDetail = (index: number, updatedNestedDetail: Detail) => {
  const updatedDetail = { ...props.detail };
  updatedDetail.details[index] = updatedNestedDetail;
  emit('update:detail', updatedDetail);
};

const removeNestedDetail = (index: number) => {
  const updatedDetail = { ...props.detail };
  updatedDetail.details.splice(index, 1);
  emit('update:detail', updatedDetail);
};
</script>

<template>
  <div
    class="detail-editor card"
    :style="{ marginLeft: `${(level || 0) * 2}px` }"
  >
    <div class="card-body">
      <div class="row">
        <input
          v-model="detail.name"
          class="form-control"
          placeholder="Detail name"
          @input="$emit('update:detail', detail)"
        />
      </div>
      <div class="row">
        <!-- <label class="form-label">Description</label> -->
        <div v-if="editor" class="container">
          <div class="control-group">
            <div class="button-group">
              <div
                class="btn-toolbar"
                role="toolbar"
                aria-label="Toolbar with button groups"
              >
                <!-- <div
                  class="btn-group"
                  role="group"
                  aria-label="Button group with nested dropdown"
                >
                  <button type="button" class="btn btn-primary">-1</button>
                  <div class="btn-group" role="group">
                    <button
                      id="btnGroupDrop1"
                      type="button"
                      class="btn btn-primary dropdown-toggle"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      H
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                      <li>
                        <a class="dropdown-item" href="#">H1</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#">H2</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#">H3</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#">H4</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#">H5</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#">H6</a>
                      </li>
                    </ul>
                  </div>
                  <button type="button" class="btn btn-primary">+1</button>
                </div> -->
                <div
                  class="btn-group btn-group-sm"
                  role="group"
                  aria-label="First group"
                >
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 1 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 1 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h1"></i>
                  </button>
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 2 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 2 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h2"></i>
                  </button>
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 3 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 3 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h3"></i>
                  </button>
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 4 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 4 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h4"></i>
                  </button>
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 5 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 5 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h5"></i>
                  </button>
                  <button
                    @click="
                      editor.chain().focus().toggleHeading({ level: 6 }).run()
                    "
                    :class="{
                      'is-active': editor.isActive('heading', { level: 6 }),
                    }"
                    class="btn btn-sm btn-outline-primary"
                  >
                    <i class="bi bi-type-h6"></i>
                  </button>
                  
                  <button
                    @click="editor.chain().focus().toggleBold().run()"
                    :disabled="!editor.can().chain().focus().toggleBold().run()"
                    :class="{ 'is-active': editor.isActive('bold') }"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="bi bi-type-bold"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().toggleItalic().run()"
                    :disabled="
                      !editor.can().chain().focus().toggleItalic().run()
                    "
                    :class="{ 'is-active': editor.isActive('italic') }"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="bi bi-type-italic"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().toggleStrike().run()"
                    :disabled="
                      !editor.can().chain().focus().toggleStrike().run()
                    "
                    :class="{ 'is-active': editor.isActive('strike') }"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="bi bi-type-strikethrough"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().toggleCode().run()"
                    :disabled="!editor.can().chain().focus().toggleCode().run()"
                    :class="{ 'is-active': editor.isActive('code') }"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    <i class="bi bi-code"></i>
                  </button>
                </div>

                
                <div
                  class="btn-group btn-group-sm" id="collapseExample"
                  role="group"
                  aria-label="third group"
                >
                  
                  <button
                    @click="editor.chain().focus().setParagraph().run()"
                    :class="{ 'is-active': editor.isActive('paragraph') }"
                    class="btn btn-sm btn-outline-info"
                  >
                    <i class="bi bi-paragraph"></i>
                  </button>

                  <button
                    @click="editor.chain().focus().toggleBulletList().run()"
                    :class="{ 'is-active': editor.isActive('bulletList') }"
                    class="btn btn-sm btn-outline-info"
                  >
                    <i class="bi bi-list-ul"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().toggleOrderedList().run()"
                    :class="{ 'is-active': editor.isActive('orderedList') }"
                    class="btn btn-sm btn-outline-info"
                  >
                    <i class="bi bi-list-ol"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().toggleCodeBlock().run()"
                    :class="{ 'is-active': editor.isActive('codeBlock') }"
                    class="btn btn-sm btn-outline-info"
                  >
                    <i class="bi bi-code-square"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().setDetails().run()"
                    :disabled="!editor.can().setDetails()"
                    class="btn btn-sm btn-outline-info"
                  >
                    <i class="bi bi-list-nested"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-info"
                    @click="editor.chain().focus().unsetDetails().run()"
                    :disabled="!editor.can().unsetDetails()"
                  >
                    <i class="bi bi-justify-left"></i>
                  </button>
                </div>
                
                  <div
                  class="btn-group btn-group-sm"
                  role="group"
                  aria-label="second group"
                >
                  <button
                    @click="editor.chain().focus().undo().run()"
                    :disabled="!editor.can().chain().focus().undo().run()"
                    class="btn btn-sm btn-light"
                  >
                    <i class="bi bi-arrow-counterclockwise"></i>
                  </button>
                  <button
                    @click="editor.chain().focus().redo().run()"
                    :disabled="!editor.can().chain().focus().redo().run()"
                    class="btn btn-sm btn-dark"
                  >
                    <i class="bi bi-arrow-clockwise"></i>
                  </button>
                </div>
                  <!-- <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample"><i class="bi bi-three-dots"></i></button> -->
                </div>

                
                
              </div>
            </div>
          
        
          <editor-content :editor="editor" />
        </div>
      </div>

      <!-- <label class="form-label">Tags</label> -->
      <div class="row">
        <div class="col-9">
          <div class="d-flex flex-wrap">
            <span
              v-for="tag in detail.tags"
              :key="tag.id"
              class="badge bg-secondary"
            >
              {{ tag.name }}
              <button
                class="btn btn-link btn-sm text-white p-0 ms-2"
                @click="removeTag(tag.id)"
              >
                ×
              </button>
            </span>
          </div>
        </div>
        <div class="col-3">
          <div class="position-relative">
            <button
              class="btn btn-outline-secondary btn-sm"
              @click="showTagSearch = !showTagSearch"
            >
              + Tag
            </button>
          </div>
        </div>
      </div>

      <div v-if="showTagSearch" class="row">
        <input
          v-model="searchQuery"
          class="form-control form-control-sm mb-2"
          placeholder="Search entities..."
        />
        <div class="list-group">
          <button
            v-for="entity in filteredEntities"
            :key="entity.id"
            class="list-group-item list-group-item-action"
            @click="addTag(entity)"
          >
            {{ entity.name }}
          </button>
        </div>
      </div>

      <hr />
      <div class="nested-details">
        <div class="row">
          <button class="btn btn-success btn-sm" @click="addNestedDetail">
            + Nested Detail
          </button>
        </div>
        <VueDraggableNext
          v-model="detail.details"
          group="nested-details"
          @change="$emit('update:detail', detail)"
        >
          <div
            v-for="(nestedDetail, index) in detail.details"
            :key="nestedDetail.id"
          >
            <div class="row">
              <div class="col-6">ID: {{ nestedDetail.id }}</div>
              <div class="col-6">
                <button
                  class="btn btn-danger btn-sm"
                  @click="removeNestedDetail(index)"
                >
                  Remove
                </button>
              </div>
            </div>
            <DetailEditor
              :detail="nestedDetail"
              :level="(level || 0) + 1"
              @update:detail="updateNestedDetail(index, $event)"
            />
          </div>
        </VueDraggableNext>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-editor {
  transition: margin-left 0.3s ease;
}
.dragArea {
  min-height: 50px;
  outline: 1px dashed;
}

.ProseMirror {
  min-height: 100px;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  padding: 0.375rem 0.75rem;
}

.ProseMirror:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Basic editor styles */
.tiptap {
  :first-child {
    margin-top: 0;
  }

  /* List styles */
  ul,
  ol {
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;
  }
  li p {
    margin-top: 0.25em;
    margin-bottom: 0.25em;
  }

  /* Heading styles */
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
    margin-top: 2.5rem;
    text-wrap: pretty;
  }

  h1,
  h2 {
    margin-top: 3.5rem;
    margin-bottom: 1.5rem;
  }

  h1 {
    font-size: 1.4rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  h3 {
    font-size: 1.1rem;
  }

  h4,
  h5,
  h6 {
    font-size: 1rem;
  }

  /* Code and preformatted text styles */
  code {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    color: var(--black);
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }

  pre {
    background: var(--black);
    border-radius: 0.5rem;
    color: var(--white);
    font-family: 'JetBrainsMono', monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;
  }
  code {
    background: none;
    color: inherit;
    font-size: 0.8rem;
    padding: 0;
  }

  blockquote {
    border-left: 3px solid var(--gray-3);
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  hr {
    border: none;
    border-top: 1px solid var(--gray-2);
    margin: 2rem 0;
  }
}
</style>
