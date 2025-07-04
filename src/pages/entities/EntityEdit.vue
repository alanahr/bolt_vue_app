<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { useEntityStore } from '../../stores/entities'
import type { Entity } from '../../types/entity';


const route = useRoute()
const router = useRouter()
const entitiesStore = useEntityStore()
const entities = ref<Entity[]>([]);

const entity = ref<Entity>({
  id: 0,
  name: '',
  entity_type: 'tool',
  entity_parent: '',
  color: '',
  icon: '',
});
  //ref<Comment[]>([])

const parentName = ref('');
const searchQuery = ref('');


onMounted(async () => {
  entities.value = await entitiesStore.getEntities();
  if (route.params.id) {
    const id = parseInt(route.params.id as string)
    const loadedEntity = await entitiesStore.getEntity(id)
    if (loadedEntity) {
      entity.value = loadedEntity
      if (loadedEntity.entity_parent) {
        const parentEntity = entities.value.find(e => e.id === loadedEntity.entity_parent.id);
        
        parentName.value = parentEntity.name
      }
    }
  }
});


const filteredEntities = computed(() => {
  return entities.value.filter(
    (entity) =>
      entity.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
    .filter(number => !excludedNumbers.includes(number));
    ;
});

const addParentEntity = (id: string) => {
  const parentEntity = entities.value.find(e => e.id === id);
  if (parentEntity) {
   entity.value.entity_parent = parentEntity
  }
}


const entityIcon = computed(() => {
  if (!entity.value) return 'bi-question-circle'
  
  switch (entity.value.entity_type) {
    case 'company': return 'bi-building fs-1'
    case 'person': return 'bi-person fs-1'
    case 'location': return 'bi-geo-alt fs-1'
    default: return 'bi-circle fs-1'
  }
})
const getEntityIcon = (type: string) => {
   if (!type) return 'bi-question-circle'
  
  switch (type) {
    case 'company': return 'bi-building fs-1'
    case 'person': return 'bi-person fs-1'
    case 'location': return 'bi-geo-alt fs-1'
    default: return 'bi-circle fs-1'
  }
}
  
const formatEntityType = (type: string) => {
  return type.charAt(0).toUpperCase() + type.slice(1)
}
  
const handleSubmit = async () => {
  if (route.params.id) {
    await entitiesStore.updateEntity(parseInt(route.params.id as string), entity.value)
  } else {
    await entitiesStore.addEntity(entity.value)
  }
  router.push('/entities')
}
</script>

<template>
  <div class="container">
    <h2>{{ route.params.id ? 'Edit' : 'Create' }} Entity</h2>
    <form @submit.prevent="handleSubmit">
      <div class="row d-flex flex-row">
        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="mb-3">
            <label for="type" class="form-label">Type</label>
            <select class="form-select" id="type" v-model="entity.entity_type">
              <option value="company">Company</option>
              <option value="object">Object</option>
              <option value="room">Room</option>
              <option value="container">Container</option>
              <option value="metadata">Metadata</option>
              <option value="person">Person</option>
              <option value="skill">Skill</option>
              <option value="tool">Tool</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
        
        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" v-model="entity.name" required>
          </div>
        </div>
        <div class="col-sm-12 col-md-6 col-lg-4">
<label for="entity_parent" class="form-label">Parent</label>
            <input type="text" class="form-control" id="" v-model="entity.entity_parent" disabled hidden>
          {{ parentName }}
        </div>
        <div class="col-sm-12 col-md-6 col-lg-4">
        <input
          v-model="searchQuery"
          class="form-control form-control-sm mb-2"
          placeholder="Search entities..."
        />
        <div class="list-group">
          <button type="button"
            v-for="entity_parent in filteredEntities"
            :key="entity_parent.id"
            class="list-group-item list-group-item-action"
            @click="addParentEntity(entity_parent.id)"
          >
            {{ entity_parent.name }}
          </button>
        </div>

        </div>
        
        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="mb-3">
            <label for="color" class="form-label">Color</label>
            <input type="color" class="form-control" id="color" v-model="entity.color">
          </div>
        </div>
        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="mb-3">
            <label for="icon" class="form-label">Icon</label>
            <input type="text" class="form-control" id="icon" v-model="entity.icon">
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Save</button>
      <router-link to="/entities" class="btn btn-secondary ms-2">Cancel</router-link>
    </form>
  </div>
  <div class="row">
    <span>
<i class="bi bi-0-circle"></i>
bi bi-0-circle
</span>
<span>
<i class="bi bi-0-square"></i>
bi bi-0-square
</span>
<span>
<i class="bi bi-1-circle"></i>
bi bi-1-circle
</span>
<span>
<i class="bi bi-1-square"></i>
bi bi-1-square
</span>
<span>
<i class="bi bi-123"></i>
bi bi-123
</span>
<span>
<i class="bi bi-2-circle"></i>
bi bi-2-circle
</span>
<span>
<i class="bi bi-2-square"></i>
bi bi-2-square
</span>
<span>
<i class="bi bi-3-circle"></i>
bi bi-3-circle
</span>
<span>
<i class="bi bi-3-square"></i>
bi bi-3-square
</span>
<span>
<i class="bi bi-4-circle"></i>
bi bi-4-circle
</span>
<span>
<i class="bi bi-4-square"></i>
bi bi-4-square
</span>
<span>
<i class="bi bi-5-circle"></i>
bi bi-5-circle
</span>
<span>
<i class="bi bi-5-square"></i>
bi bi-5-square
</span>
<span>
<i class="bi bi-6-circle"></i>
bi bi-6-circle
</span>
<span>
<i class="bi bi-6-square"></i>
bi bi-6-square
</span>
<span>
<i class="bi bi-7-circle"></i>
bi bi-7-circle
</span>
<span>
<i class="bi bi-7-square"></i>
bi bi-7-square
</span>
<span>
<i class="bi bi-8-circle"></i>
bi bi-8-circle
</span>
<span>
<i class="bi bi-8-square"></i>
bi bi-8-square
</span>
<span>
<i class="bi bi-9-circle"></i>
bi bi-9-circle
</span>
<span>
<i class="bi bi-9-square"></i>
bi bi-9-square
</span>
<span>
<i class="bi bi-activity"></i>
bi bi-activity
</span>
<span>
<i class="bi bi-airplane"></i>
bi bi-airplane
</span>
<span>
<i class="bi bi-airplane-engines"></i>
bi bi-airplane-engines
</span>
<span>
<i class="bi bi-alarm"></i>
bi bi-alarm
</span>
<span>
<i class="bi bi-alexa"></i>
bi bi-alexa
</span>
<span>
<i class="bi bi-align-bottom"></i>
bi bi-align-bottom
</span>
<span>
<i class="bi bi-align-center"></i>
bi bi-align-center
</span>
<span>
<i class="bi bi-align-end"></i>
bi bi-align-end
</span>
<span>
<i class="bi bi-align-middle"></i>
bi bi-align-middle
</span>
<span>
<i class="bi bi-align-start"></i>
bi bi-align-start
</span>
<span>
<i class="bi bi-align-top"></i>
bi bi-align-top
</span>
<span>
<i class="bi bi-alipay"></i>
bi bi-alipay
</span>
<span>
<i class="bi bi-alphabet"></i>
bi bi-alphabet
</span>
<span>
<i class="bi bi-alphabet-uppercase"></i>
bi bi-alphabet-uppercase
</span>
<span>
<i class="bi bi-alt"></i>
bi bi-alt
</span>
<span>
<i class="bi bi-amazon"></i>
bi bi-amazon
</span>
<span>
<i class="bi bi-amd"></i>
bi bi-amd
</span>
<span>
<i class="bi bi-android"></i>
bi bi-android
</span>
<span>
<i class="bi bi-android2"></i>
bi bi-android2
</span>
<span>
<i class="bi bi-anthropic"></i>
bi bi-anthropic
</span>
<span>
<i class="bi bi-app"></i>
bi bi-app
</span>
<span>
<i class="bi bi-app-indicator"></i>
bi bi-app-indicator
</span>
<span>
<i class="bi bi-apple"></i>
bi bi-apple
</span>
<span>
<i class="bi bi-apple-music"></i>
bi bi-apple-music
</span>
<span>
<i class="bi bi-archive"></i>
bi bi-archive
</span>
<span>
<i class="bi bi-arrow-90deg-down"></i>
bi bi-arrow-90deg-down
</span>
<span>
<i class="bi bi-arrow-90deg-left"></i>
bi bi-arrow-90deg-left
</span>
<span>
<i class="bi bi-arrow-90deg-right"></i>
bi bi-arrow-90deg-right
</span>
<span>
<i class="bi bi-arrow-90deg-up"></i>
bi bi-arrow-90deg-up
</span>
<span>
<i class="bi bi-arrow-bar-down"></i>
bi bi-arrow-bar-down
</span>
<span>
<i class="bi bi-arrow-bar-left"></i>
bi bi-arrow-bar-left
</span>
<span>
<i class="bi bi-arrow-bar-right"></i>
bi bi-arrow-bar-right
</span>
<span>
<i class="bi bi-arrow-bar-up"></i>
bi bi-arrow-bar-up
</span>
<span>
<i class="bi bi-arrow-clockwise"></i>
bi bi-arrow-clockwise
</span>
<span>
<i class="bi bi-arrow-counterclockwise"></i>
bi bi-arrow-counterclockwise
</span>
<span>
<i class="bi bi-arrow-down"></i>
bi bi-arrow-down
</span>
<span>
<i class="bi bi-arrow-down-circle"></i>
bi bi-arrow-down-circle
</span>
<span>
<i class="bi bi-arrow-down-left-circle"></i>
bi bi-arrow-down-left-circle
</span>
<span>
<i class="bi bi-arrow-down-left-square"></i>
bi bi-arrow-down-left-square
</span>
<span>
<i class="bi bi-arrow-down-right-circle"></i>
bi bi-arrow-down-right-circle
</span>
<span>
<i class="bi bi-arrow-down-right-square"></i>
bi bi-arrow-down-right-square
</span>
<span>
<i class="bi bi-arrow-down-square"></i>
bi bi-arrow-down-square
</span>
<span>
<i class="bi bi-arrow-down-left"></i>
bi bi-arrow-down-left
</span>
<span>
<i class="bi bi-arrow-down-right"></i>
bi bi-arrow-down-right
</span>
<span>
<i class="bi bi-arrow-down-short"></i>
bi bi-arrow-down-short
</span>
<span>
<i class="bi bi-arrow-down-up"></i>
bi bi-arrow-down-up
</span>
<span>
<i class="bi bi-arrow-left"></i>
bi bi-arrow-left
</span>
<span>
<i class="bi bi-arrow-left-circle"></i>
bi bi-arrow-left-circle
</span>
<span>
<i class="bi bi-arrow-left-square"></i>
bi bi-arrow-left-square
</span>
<span>
<i class="bi bi-arrow-left-right"></i>
bi bi-arrow-left-right
</span>
<span>
<i class="bi bi-arrow-left-short"></i>
bi bi-arrow-left-short
</span>
<span>
<i class="bi bi-arrow-repeat"></i>
bi bi-arrow-repeat
</span>
<span>
<i class="bi bi-arrow-return-left"></i>
bi bi-arrow-return-left
</span>
<span>
<i class="bi bi-arrow-return-right"></i>
bi bi-arrow-return-right
</span>
<span>
<i class="bi bi-arrow-right"></i>
bi bi-arrow-right
</span>
<span>
<i class="bi bi-arrow-right-circle"></i>
bi bi-arrow-right-circle
</span>
<span>
<i class="bi bi-arrow-right-square"></i>
bi bi-arrow-right-square
</span>
<span>
<i class="bi bi-arrow-right-short"></i>
bi bi-arrow-right-short
</span>
<span>
<i class="bi bi-arrow-through-heart"></i>
bi bi-arrow-through-heart
</span>
<span>
<i class="bi bi-arrow-up"></i>
bi bi-arrow-up
</span>
<span>
<i class="bi bi-arrow-up-circle"></i>
bi bi-arrow-up-circle
</span>
<span>
<i class="bi bi-arrow-up-left-circle"></i>
bi bi-arrow-up-left-circle
</span>
<span>
<i class="bi bi-arrow-up-left-square"></i>
bi bi-arrow-up-left-square
</span>
<span>
<i class="bi bi-arrow-up-right-circle"></i>
bi bi-arrow-up-right-circle
</span>
<span>
<i class="bi bi-arrow-up-right-square"></i>
bi bi-arrow-up-right-square
</span>
<span>
<i class="bi bi-arrow-up-square"></i>
bi bi-arrow-up-square
</span>
<span>
<i class="bi bi-arrow-up-left"></i>
bi bi-arrow-up-left
</span>
<span>
<i class="bi bi-arrow-up-right"></i>
bi bi-arrow-up-right
</span>
<span>
<i class="bi bi-arrow-up-short"></i>
bi bi-arrow-up-short
</span>
<span>
<i class="bi bi-arrows"></i>
bi bi-arrows
</span>
<span>
<i class="bi bi-arrows-angle-contract"></i>
bi bi-arrows-angle-contract
</span>
<span>
<i class="bi bi-arrows-angle-expand"></i>
bi bi-arrows-angle-expand
</span>
<span>
<i class="bi bi-arrows-collapse"></i>
bi bi-arrows-collapse
</span>
<span>
<i class="bi bi-arrows-collapse-vertical"></i>
bi bi-arrows-collapse-vertical
</span>
<span>
<i class="bi bi-arrows-expand"></i>
bi bi-arrows-expand
</span>
<span>
<i class="bi bi-arrows-expand-vertical"></i>
bi bi-arrows-expand-vertical
</span>
<span>
<i class="bi bi-arrows-fullscreen"></i>
bi bi-arrows-fullscreen
</span>
<span>
<i class="bi bi-arrows-move"></i>
bi bi-arrows-move
</span>
<span>
<i class="bi bi-arrows-vertical"></i>
bi bi-arrows-vertical
</span>
<span>
<i class="bi bi-aspect-ratio"></i>
bi bi-aspect-ratio
</span>
<span>
<i class="bi bi-asterisk"></i>
bi bi-asterisk
</span>
<span>
<i class="bi bi-at"></i>
bi bi-at
</span>
<span>
<i class="bi bi-award"></i>
bi bi-award
</span>
<span>
<i class="bi bi-back"></i>
bi bi-back
</span>
<span>
<i class="bi bi-backpack"></i>
bi bi-backpack
</span>
<span>
<i class="bi bi-backpack2"></i>
bi bi-backpack2
</span>
<span>
<i class="bi bi-backpack3"></i>
bi bi-backpack3
</span>
<span>
<i class="bi bi-backpack4"></i>
bi bi-backpack4
</span>
<span>
<i class="bi bi-backspace"></i>
bi bi-backspace
</span>
<span>
<i class="bi bi-backspace-reverse"></i>
bi bi-backspace-reverse
</span>
<span>
<i class="bi bi-badge-3d"></i>
bi bi-badge-3d
</span>
<span>
<i class="bi bi-badge-4k"></i>
bi bi-badge-4k
</span>
<span>
<i class="bi bi-badge-8k"></i>
bi bi-badge-8k
</span>
<span>
<i class="bi bi-badge-ad"></i>
bi bi-badge-ad
</span>
<span>
<i class="bi bi-badge-ar"></i>
bi bi-badge-ar
</span>
<span>
<i class="bi bi-badge-cc"></i>
bi bi-badge-cc
</span>
<span>
<i class="bi bi-badge-hd"></i>
bi bi-badge-hd
</span>
<span>
<i class="bi bi-badge-sd"></i>
bi bi-badge-sd
</span>
<span>
<i class="bi bi-badge-tm"></i>
bi bi-badge-tm
</span>
<span>
<i class="bi bi-badge-vo"></i>
bi bi-badge-vo
</span>
<span>
<i class="bi bi-badge-vr"></i>
bi bi-badge-vr
</span>
<span>
<i class="bi bi-badge-wc"></i>
bi bi-badge-wc
</span>
<span>
<i class="bi bi-bag"></i>
bi bi-bag
</span>
<span>
<i class="bi bi-bag-check"></i>
bi bi-bag-check
</span>
<span>
<i class="bi bi-bag-dash"></i>
bi bi-bag-dash
</span>
<span>
<i class="bi bi-bag-heart"></i>
bi bi-bag-heart
</span>
<span>
<i class="bi bi-bag-plus"></i>
bi bi-bag-plus
</span>
<span>
<i class="bi bi-bag-x"></i>
bi bi-bag-x
</span>
<span>
<i class="bi bi-balloon"></i>
bi bi-balloon
</span>
<span>
<i class="bi bi-balloon-heart"></i>
bi bi-balloon-heart
</span>
<span>
<i class="bi bi-ban"></i>
bi bi-ban
</span>
<span>
<i class="bi bi-bandaid"></i>
bi bi-bandaid
</span>
<span>
<i class="bi bi-bank"></i>
bi bi-bank
</span>
<span>
<i class="bi bi-bank2"></i>
bi bi-bank2
</span>
<span>
<i class="bi bi-bar-chart"></i>
bi bi-bar-chart
</span>
<span>
<i class="bi bi-bar-chart-line"></i>
bi bi-bar-chart-line
</span>
<span>
<i class="bi bi-bar-chart-steps"></i>
bi bi-bar-chart-steps
</span>
<span>
<i class="bi bi-basket"></i>
bi bi-basket
</span>
<span>
<i class="bi bi-basket2"></i>
bi bi-basket2
</span>
<span>
<i class="bi bi-basket3"></i>
bi bi-basket3
</span>
<span>
<i class="bi bi-battery"></i>
bi bi-battery
</span>
<span>
<i class="bi bi-battery-charging"></i>
bi bi-battery-charging
</span>
<span>
<i class="bi bi-battery-full"></i>
bi bi-battery-full
</span>
<span>
<i class="bi bi-battery-half"></i>
bi bi-battery-half
</span>
<span>
<i class="bi bi-battery-low"></i>
bi bi-battery-low
</span>
<span>
<i class="bi bi-beaker"></i>
bi bi-beaker
</span>
<span>
<i class="bi bi-behance"></i>
bi bi-behance
</span>
<span>
<i class="bi bi-bell"></i>
bi bi-bell
</span>
<span>
<i class="bi bi-bell-slash"></i>
bi bi-bell-slash
</span>
<span>
<i class="bi bi-bezier"></i>
bi bi-bezier
</span>
<span>
<i class="bi bi-bezier2"></i>
bi bi-bezier2
</span>
<span>
<i class="bi bi-bicycle"></i>
bi bi-bicycle
</span>
<span>
<i class="bi bi-bing"></i>
bi bi-bing
</span>
<span>
<i class="bi bi-binoculars"></i>
bi bi-binoculars
</span>
<span>
<i class="bi bi-blockquote-left"></i>
bi bi-blockquote-left
</span>
<span>
<i class="bi bi-blockquote-right"></i>
bi bi-blockquote-right
</span>
<span>
<i class="bi bi-bluesky"></i>
bi bi-bluesky
</span>
<span>
<i class="bi bi-bluetooth"></i>
bi bi-bluetooth
</span>
<span>
<i class="bi bi-body-text"></i>
bi bi-body-text
</span>
<span>
<i class="bi bi-book"></i>
bi bi-book
</span>
<span>
<i class="bi bi-book-half"></i>
bi bi-book-half
</span>
<span>
<i class="bi bi-bookmark"></i>
bi bi-bookmark
</span>
<span>
<i class="bi bi-bookmark-check"></i>
bi bi-bookmark-check
</span>
<span>
<i class="bi bi-bookmark-dash"></i>
bi bi-bookmark-dash
</span>
<span>
<i class="bi bi-bookmark-heart"></i>
bi bi-bookmark-heart
</span>
<span>
<i class="bi bi-bookmark-plus"></i>
bi bi-bookmark-plus
</span>
<span>
<i class="bi bi-bookmark-star"></i>
bi bi-bookmark-star
</span>
<span>
<i class="bi bi-bookmark-x"></i>
bi bi-bookmark-x
</span>
<span>
<i class="bi bi-bookmarks"></i>
bi bi-bookmarks
</span>
<span>
<i class="bi bi-bookshelf"></i>
bi bi-bookshelf
</span>
<span>
<i class="bi bi-boombox"></i>
bi bi-boombox
</span>
<span>
<i class="bi bi-bootstrap"></i>
bi bi-bootstrap
</span>
<span>
<i class="bi bi-bootstrap-reboot"></i>
bi bi-bootstrap-reboot
</span>
<span>
<i class="bi bi-border"></i>
bi bi-border
</span>
<span>
<i class="bi bi-border-all"></i>
bi bi-border-all
</span>
<span>
<i class="bi bi-border-bottom"></i>
bi bi-border-bottom
</span>
<span>
<i class="bi bi-border-center"></i>
bi bi-border-center
</span>
<span>
<i class="bi bi-border-inner"></i>
bi bi-border-inner
</span>
<span>
<i class="bi bi-border-left"></i>
bi bi-border-left
</span>
<span>
<i class="bi bi-border-middle"></i>
bi bi-border-middle
</span>
<span>
<i class="bi bi-border-outer"></i>
bi bi-border-outer
</span>
<span>
<i class="bi bi-border-right"></i>
bi bi-border-right
</span>
<span>
<i class="bi bi-border-style"></i>
bi bi-border-style
</span>
<span>
<i class="bi bi-border-top"></i>
bi bi-border-top
</span>
<span>
<i class="bi bi-border-width"></i>
bi bi-border-width
</span>
<span>
<i class="bi bi-bounding-box"></i>
bi bi-bounding-box
</span>
<span>
<i class="bi bi-bounding-box-circles"></i>
bi bi-bounding-box-circles
</span>
<span>
<i class="bi bi-box"></i>
bi bi-box
</span>
<span>
<i class="bi bi-box-arrow-down-left"></i>
bi bi-box-arrow-down-left
</span>
<span>
<i class="bi bi-box-arrow-down-right"></i>
bi bi-box-arrow-down-right
</span>
<span>
<i class="bi bi-box-arrow-down"></i>
bi bi-box-arrow-down
</span>
<span>
<i class="bi bi-box-arrow-in-down"></i>
bi bi-box-arrow-in-down
</span>
<span>
<i class="bi bi-box-arrow-in-down-left"></i>
bi bi-box-arrow-in-down-left
</span>
<span>
<i class="bi bi-box-arrow-in-down-right"></i>
bi bi-box-arrow-in-down-right
</span>
<span>
<i class="bi bi-box-arrow-in-left"></i>
bi bi-box-arrow-in-left
</span>
<span>
<i class="bi bi-box-arrow-in-right"></i>
bi bi-box-arrow-in-right
</span>
<span>
<i class="bi bi-box-arrow-in-up"></i>
bi bi-box-arrow-in-up
</span>
<span>
<i class="bi bi-box-arrow-in-up-left"></i>
bi bi-box-arrow-in-up-left
</span>
<span>
<i class="bi bi-box-arrow-in-up-right"></i>
bi bi-box-arrow-in-up-right
</span>
<span>
<i class="bi bi-box-arrow-left"></i>
bi bi-box-arrow-left
</span>
<span>
<i class="bi bi-box-arrow-right"></i>
bi bi-box-arrow-right
</span>
<span>
<i class="bi bi-box-arrow-up"></i>
bi bi-box-arrow-up
</span>
<span>
<i class="bi bi-box-arrow-up-left"></i>
bi bi-box-arrow-up-left
</span>
<span>
<i class="bi bi-box-arrow-up-right"></i>
bi bi-box-arrow-up-right
</span>
<span>
<i class="bi bi-box-seam"></i>
bi bi-box-seam
</span>
<span>
<i class="bi bi-box2"></i>
bi bi-box2
</span>
<span>
<i class="bi bi-box2-heart"></i>
bi bi-box2-heart
</span>
<span>
<i class="bi bi-boxes"></i>
bi bi-boxes
</span>
<span>
<i class="bi bi-braces"></i>
bi bi-braces
</span>
<span>
<i class="bi bi-braces-asterisk"></i>
bi bi-braces-asterisk
</span>
<span>
<i class="bi bi-bricks"></i>
bi bi-bricks
</span>
<span>
<i class="bi bi-briefcase"></i>
bi bi-briefcase
</span>
<span>
<i class="bi bi-brightness-alt-high"></i>
bi bi-brightness-alt-high
</span>
<span>
<i class="bi bi-brightness-alt-low"></i>
bi bi-brightness-alt-low
</span>
<span>
<i class="bi bi-brightness-high"></i>
bi bi-brightness-high
</span>
<span>
<i class="bi bi-brightness-low"></i>
bi bi-brightness-low
</span>
<span>
<i class="bi bi-brilliance"></i>
bi bi-brilliance
</span>
<span>
<i class="bi bi-broadcast"></i>
bi bi-broadcast
</span>
<span>
<i class="bi bi-broadcast-pin"></i>
bi bi-broadcast-pin
</span>
<span>
<i class="bi bi-browser-chrome"></i>
bi bi-browser-chrome
</span>
<span>
<i class="bi bi-browser-edge"></i>
bi bi-browser-edge
</span>
<span>
<i class="bi bi-browser-firefox"></i>
bi bi-browser-firefox
</span>
<span>
<i class="bi bi-browser-safari"></i>
bi bi-browser-safari
</span>
<span>
<i class="bi bi-brush"></i>
bi bi-brush
</span>
<span>
<i class="bi bi-bucket"></i>
bi bi-bucket
</span>
<span>
<i class="bi bi-bug"></i>
bi bi-bug
</span>
<span>
<i class="bi bi-building"></i>
bi bi-building
</span>
<span>
<i class="bi bi-building-add"></i>
bi bi-building-add
</span>
<span>
<i class="bi bi-building-check"></i>
bi bi-building-check
</span>
<span>
<i class="bi bi-building-dash"></i>
bi bi-building-dash
</span>
<span>
<i class="bi bi-building-down"></i>
bi bi-building-down
</span>
<span>
<i class="bi bi-building-exclamation"></i>
bi bi-building-exclamation
</span>
<span>
<i class="bi bi-building-gear"></i>
bi bi-building-gear
</span>
<span>
<i class="bi bi-building-lock"></i>
bi bi-building-lock
</span>
<span>
<i class="bi bi-building-slash"></i>
bi bi-building-slash
</span>
<span>
<i class="bi bi-building-up"></i>
bi bi-building-up
</span>
<span>
<i class="bi bi-building-x"></i>
bi bi-building-x
</span>
<span>
<i class="bi bi-buildings"></i>
bi bi-buildings
</span>
<span>
<i class="bi bi-bullseye"></i>
bi bi-bullseye
</span>
<span>
<i class="bi bi-bus-front"></i>
bi bi-bus-front
</span>
<span>
<i class="bi bi-c-circle"></i>
bi bi-c-circle
</span>
<span>
<i class="bi bi-c-square"></i>
bi bi-c-square
</span>
<span>
<i class="bi bi-cake"></i>
bi bi-cake
</span>
<span>
<i class="bi bi-cake2"></i>
bi bi-cake2
</span>
<span>
<i class="bi bi-calculator"></i>
bi bi-calculator
</span>
<span>
<i class="bi bi-calendar"></i>
bi bi-calendar
</span>
<span>
<i class="bi bi-calendar-check"></i>
bi bi-calendar-check
</span>
<span>
<i class="bi bi-calendar-date"></i>
bi bi-calendar-date
</span>
<span>
<i class="bi bi-calendar-day"></i>
bi bi-calendar-day
</span>
<span>
<i class="bi bi-calendar-event"></i>
bi bi-calendar-event
</span>
<span>
<i class="bi bi-calendar-heart"></i>
bi bi-calendar-heart
</span>
<span>
<i class="bi bi-calendar-minus"></i>
bi bi-calendar-minus
</span>
<span>
<i class="bi bi-calendar-month"></i>
bi bi-calendar-month
</span>
<span>
<i class="bi bi-calendar-plus"></i>
bi bi-calendar-plus
</span>
<span>
<i class="bi bi-calendar-range"></i>
bi bi-calendar-range
</span>
<span>
<i class="bi bi-calendar-week"></i>
bi bi-calendar-week
</span>
<span>
<i class="bi bi-calendar-x"></i>
bi bi-calendar-x
</span>
<span>
<i class="bi bi-calendar2"></i>
bi bi-calendar2
</span>
<span>
<i class="bi bi-calendar2-check"></i>
bi bi-calendar2-check
</span>
<span>
<i class="bi bi-calendar2-date"></i>
bi bi-calendar2-date
</span>
<span>
<i class="bi bi-calendar2-day"></i>
bi bi-calendar2-day
</span>
<span>
<i class="bi bi-calendar2-event"></i>
bi bi-calendar2-event
</span>
<span>
<i class="bi bi-calendar2-heart"></i>
bi bi-calendar2-heart
</span>
<span>
<i class="bi bi-calendar2-minus"></i>
bi bi-calendar2-minus
</span>
<span>
<i class="bi bi-calendar2-month"></i>
bi bi-calendar2-month
</span>
<span>
<i class="bi bi-calendar2-plus"></i>
bi bi-calendar2-plus
</span>
<span>
<i class="bi bi-calendar2-range"></i>
bi bi-calendar2-range
</span>
<span>
<i class="bi bi-calendar2-week"></i>
bi bi-calendar2-week
</span>
<span>
<i class="bi bi-calendar2-x"></i>
bi bi-calendar2-x
</span>
<span>
<i class="bi bi-calendar3"></i>
bi bi-calendar3
</span>
<span>
<i class="bi bi-calendar3-event"></i>
bi bi-calendar3-event
</span>
<span>
<i class="bi bi-calendar3-range"></i>
bi bi-calendar3-range
</span>
<span>
<i class="bi bi-calendar3-week"></i>
bi bi-calendar3-week
</span>
<span>
<i class="bi bi-calendar4"></i>
bi bi-calendar4
</span>
<span>
<i class="bi bi-calendar4-event"></i>
bi bi-calendar4-event
</span>
<span>
<i class="bi bi-calendar4-range"></i>
bi bi-calendar4-range
</span>
<span>
<i class="bi bi-calendar4-week"></i>
bi bi-calendar4-week
</span>
<span>
<i class="bi bi-camera"></i>
bi bi-camera
</span>
<span>
<i class="bi bi-camera2"></i>
bi bi-camera2
</span>
<span>
<i class="bi bi-camera-reels"></i>
bi bi-camera-reels
</span>
<span>
<i class="bi bi-camera-video"></i>
bi bi-camera-video
</span>
<span>
<i class="bi bi-camera-video-off"></i>
bi bi-camera-video-off
</span>
<span>
<i class="bi bi-capslock"></i>
bi bi-capslock
</span>
<span>
<i class="bi bi-capsule"></i>
bi bi-capsule
</span>
<span>
<i class="bi bi-capsule-pill"></i>
bi bi-capsule-pill
</span>
<span>
<i class="bi bi-car-front"></i>
bi bi-car-front
</span>
<span>
<i class="bi bi-card-checklist"></i>
bi bi-card-checklist
</span>
<span>
<i class="bi bi-card-heading"></i>
bi bi-card-heading
</span>
<span>
<i class="bi bi-card-image"></i>
bi bi-card-image
</span>
<span>
<i class="bi bi-card-list"></i>
bi bi-card-list
</span>
<span>
<i class="bi bi-card-text"></i>
bi bi-card-text
</span>
<span>
<i class="bi bi-caret-down"></i>
bi bi-caret-down
</span>
<span>
<i class="bi bi-caret-down-square"></i>
bi bi-caret-down-square
</span>
<span>
<i class="bi bi-caret-left"></i>
bi bi-caret-left
</span>
<span>
<i class="bi bi-caret-left-square"></i>
bi bi-caret-left-square
</span>
<span>
<i class="bi bi-caret-right"></i>
bi bi-caret-right
</span>
<span>
<i class="bi bi-caret-right-square"></i>
bi bi-caret-right-square
</span>
<span>
<i class="bi bi-caret-up"></i>
bi bi-caret-up
</span>
<span>
<i class="bi bi-caret-up-square"></i>
bi bi-caret-up-square
</span>
<span>
<i class="bi bi-cart"></i>
bi bi-cart
</span>
<span>
<i class="bi bi-cart-check"></i>
bi bi-cart-check
</span>
<span>
<i class="bi bi-cart-dash"></i>
bi bi-cart-dash
</span>
<span>
<i class="bi bi-cart-plus"></i>
bi bi-cart-plus
</span>
<span>
<i class="bi bi-cart-x"></i>
bi bi-cart-x
</span>
<span>
<i class="bi bi-cart2"></i>
bi bi-cart2
</span>
<span>
<i class="bi bi-cart3"></i>
bi bi-cart3
</span>
<span>
<i class="bi bi-cart4"></i>
bi bi-cart4
</span>
<span>
<i class="bi bi-cash"></i>
bi bi-cash
</span>
<span>
<i class="bi bi-cash-coin"></i>
bi bi-cash-coin
</span>
<span>
<i class="bi bi-cash-stack"></i>
bi bi-cash-stack
</span>
<span>
<i class="bi bi-cassette"></i>
bi bi-cassette
</span>
<span>
<i class="bi bi-cast"></i>
bi bi-cast
</span>
<span>
<i class="bi bi-cc-circle"></i>
bi bi-cc-circle
</span>
<span>
<i class="bi bi-cc-square"></i>
bi bi-cc-square
</span>
<span>
<i class="bi bi-chat"></i>
bi bi-chat
</span>
<span>
<i class="bi bi-chat-dots"></i>
bi bi-chat-dots
</span>
<span>
<i class="bi bi-chat-heart"></i>
bi bi-chat-heart
</span>
<span>
<i class="bi bi-chat-left"></i>
bi bi-chat-left
</span>
<span>
<i class="bi bi-chat-left-dots"></i>
bi bi-chat-left-dots
</span>
<span>
<i class="bi bi-chat-left-heart"></i>
bi bi-chat-left-heart
</span>
<span>
<i class="bi bi-chat-left-quote"></i>
bi bi-chat-left-quote
</span>
<span>
<i class="bi bi-chat-left-text"></i>
bi bi-chat-left-text
</span>
<span>
<i class="bi bi-chat-quote"></i>
bi bi-chat-quote
</span>
<span>
<i class="bi bi-chat-right"></i>
bi bi-chat-right
</span>
<span>
<i class="bi bi-chat-right-dots"></i>
bi bi-chat-right-dots
</span>
<span>
<i class="bi bi-chat-right-heart"></i>
bi bi-chat-right-heart
</span>
<span>
<i class="bi bi-chat-right-quote"></i>
bi bi-chat-right-quote
</span>
<span>
<i class="bi bi-chat-right-text"></i>
bi bi-chat-right-text
</span>
<span>
<i class="bi bi-chat-square"></i>
bi bi-chat-square
</span>
<span>
<i class="bi bi-chat-square-dots"></i>
bi bi-chat-square-dots
</span>
<span>
<i class="bi bi-chat-square-heart"></i>
bi bi-chat-square-heart
</span>
<span>
<i class="bi bi-chat-square-quote"></i>
bi bi-chat-square-quote
</span>
<span>
<i class="bi bi-chat-square-text"></i>
bi bi-chat-square-text
</span>
<span>
<i class="bi bi-chat-text"></i>
bi bi-chat-text
</span>
<span>
<i class="bi bi-check"></i>
bi bi-check
</span>
<span>
<i class="bi bi-check-all"></i>
bi bi-check-all
</span>
<span>
<i class="bi bi-check-circle"></i>
bi bi-check-circle
</span>
<span>
<i class="bi bi-check-lg"></i>
bi bi-check-lg
</span>
<span>
<i class="bi bi-check-square"></i>
bi bi-check-square
</span>
<span>
<i class="bi bi-check2"></i>
bi bi-check2
</span>
<span>
<i class="bi bi-check2-all"></i>
bi bi-check2-all
</span>
<span>
<i class="bi bi-check2-circle"></i>
bi bi-check2-circle
</span>
<span>
<i class="bi bi-check2-square"></i>
bi bi-check2-square
</span>
<span>
<i class="bi bi-chevron-bar-contract"></i>
bi bi-chevron-bar-contract
</span>
<span>
<i class="bi bi-chevron-bar-down"></i>
bi bi-chevron-bar-down
</span>
<span>
<i class="bi bi-chevron-bar-expand"></i>
bi bi-chevron-bar-expand
</span>
<span>
<i class="bi bi-chevron-bar-left"></i>
bi bi-chevron-bar-left
</span>
<span>
<i class="bi bi-chevron-bar-right"></i>
bi bi-chevron-bar-right
</span>
<span>
<i class="bi bi-chevron-bar-up"></i>
bi bi-chevron-bar-up
</span>
<span>
<i class="bi bi-chevron-compact-down"></i>
bi bi-chevron-compact-down
</span>
<span>
<i class="bi bi-chevron-compact-left"></i>
bi bi-chevron-compact-left
</span>
<span>
<i class="bi bi-chevron-compact-right"></i>
bi bi-chevron-compact-right
</span>
<span>
<i class="bi bi-chevron-compact-up"></i>
bi bi-chevron-compact-up
</span>
<span>
<i class="bi bi-chevron-contract"></i>
bi bi-chevron-contract
</span>
<span>
<i class="bi bi-chevron-double-down"></i>
bi bi-chevron-double-down
</span>
<span>
<i class="bi bi-chevron-double-left"></i>
bi bi-chevron-double-left
</span>
<span>
<i class="bi bi-chevron-double-right"></i>
bi bi-chevron-double-right
</span>
<span>
<i class="bi bi-chevron-double-up"></i>
bi bi-chevron-double-up
</span>
<span>
<i class="bi bi-chevron-down"></i>
bi bi-chevron-down
</span>
<span>
<i class="bi bi-chevron-expand"></i>
bi bi-chevron-expand
</span>
<span>
<i class="bi bi-chevron-left"></i>
bi bi-chevron-left
</span>
<span>
<i class="bi bi-chevron-right"></i>
bi bi-chevron-right
</span>
<span>
<i class="bi bi-chevron-up"></i>
bi bi-chevron-up
</span>
<span>
<i class="bi bi-circle"></i>
bi bi-circle
</span>
<span>
<i class="bi bi-circle-half"></i>
bi bi-circle-half
</span>
<span>
<i class="bi bi-slash-circle"></i>
bi bi-slash-circle
</span>
<span>
<i class="bi bi-circle-square"></i>
bi bi-circle-square
</span>
<span>
<i class="bi bi-claude"></i>
bi bi-claude
</span>
<span>
<i class="bi bi-clipboard"></i>
bi bi-clipboard
</span>
<span>
<i class="bi bi-clipboard-check"></i>
bi bi-clipboard-check
</span>
<span>
<i class="bi bi-clipboard-data"></i>
bi bi-clipboard-data
</span>
<span>
<i class="bi bi-clipboard-heart"></i>
bi bi-clipboard-heart
</span>
<span>
<i class="bi bi-clipboard-minus"></i>
bi bi-clipboard-minus
</span>
<span>
<i class="bi bi-clipboard-plus"></i>
bi bi-clipboard-plus
</span>
<span>
<i class="bi bi-clipboard-pulse"></i>
bi bi-clipboard-pulse
</span>
<span>
<i class="bi bi-clipboard-x"></i>
bi bi-clipboard-x
</span>
<span>
<i class="bi bi-clipboard2"></i>
bi bi-clipboard2
</span>
<span>
<i class="bi bi-clipboard2-check"></i>
bi bi-clipboard2-check
</span>
<span>
<i class="bi bi-clipboard2-data"></i>
bi bi-clipboard2-data
</span>
<span>
<i class="bi bi-clipboard2-heart"></i>
bi bi-clipboard2-heart
</span>
<span>
<i class="bi bi-clipboard2-minus"></i>
bi bi-clipboard2-minus
</span>
<span>
<i class="bi bi-clipboard2-plus"></i>
bi bi-clipboard2-plus
</span>
<span>
<i class="bi bi-clipboard2-pulse"></i>
bi bi-clipboard2-pulse
</span>
<span>
<i class="bi bi-clipboard2-x"></i>
bi bi-clipboard2-x
</span>
<span>
<i class="bi bi-clock"></i>
bi bi-clock
</span>
<span>
<i class="bi bi-clock-history"></i>
bi bi-clock-history
</span>
<span>
<i class="bi bi-cloud"></i>
bi bi-cloud
</span>
<span>
<i class="bi bi-cloud-arrow-down"></i>
bi bi-cloud-arrow-down
</span>
<span>
<i class="bi bi-cloud-arrow-up"></i>
bi bi-cloud-arrow-up
</span>
<span>
<i class="bi bi-cloud-check"></i>
bi bi-cloud-check
</span>
<span>
<i class="bi bi-cloud-download"></i>
bi bi-cloud-download
</span>
<span>
<i class="bi bi-cloud-drizzle"></i>
bi bi-cloud-drizzle
</span>
<span>
<i class="bi bi-cloud-fog"></i>
bi bi-cloud-fog
</span>
<span>
<i class="bi bi-cloud-fog2"></i>
bi bi-cloud-fog2
</span>
<span>
<i class="bi bi-cloud-hail"></i>
bi bi-cloud-hail
</span>
<span>
<i class="bi bi-cloud-haze"></i>
bi bi-cloud-haze
</span>
<span>
<i class="bi bi-cloud-haze2"></i>
bi bi-cloud-haze2
</span>
<span>
<i class="bi bi-cloud-lightning"></i>
bi bi-cloud-lightning
</span>
<span>
<i class="bi bi-cloud-lightning-rain"></i>
bi bi-cloud-lightning-rain
</span>
<span>
<i class="bi bi-cloud-minus"></i>
bi bi-cloud-minus
</span>
<span>
<i class="bi bi-cloud-moon"></i>
bi bi-cloud-moon
</span>
<span>
<i class="bi bi-cloud-plus"></i>
bi bi-cloud-plus
</span>
<span>
<i class="bi bi-cloud-rain"></i>
bi bi-cloud-rain
</span>
<span>
<i class="bi bi-cloud-rain-heavy"></i>
bi bi-cloud-rain-heavy
</span>
<span>
<i class="bi bi-cloud-slash"></i>
bi bi-cloud-slash
</span>
<span>
<i class="bi bi-cloud-sleet"></i>
bi bi-cloud-sleet
</span>
<span>
<i class="bi bi-cloud-snow"></i>
bi bi-cloud-snow
</span>
<span>
<i class="bi bi-cloud-sun"></i>
bi bi-cloud-sun
</span>
<span>
<i class="bi bi-cloud-upload"></i>
bi bi-cloud-upload
</span>
<span>
<i class="bi bi-clouds"></i>
bi bi-clouds
</span>
<span>
<i class="bi bi-cloudy"></i>
bi bi-cloudy
</span>
<span>
<i class="bi bi-code"></i>
bi bi-code
</span>
<span>
<i class="bi bi-code-slash"></i>
bi bi-code-slash
</span>
<span>
<i class="bi bi-code-square"></i>
bi bi-code-square
</span>
<span>
<i class="bi bi-coin"></i>
bi bi-coin
</span>
<span>
<i class="bi bi-collection"></i>
bi bi-collection
</span>
<span>
<i class="bi bi-collection-play"></i>
bi bi-collection-play
</span>
<span>
<i class="bi bi-columns"></i>
bi bi-columns
</span>
<span>
<i class="bi bi-columns-gap"></i>
bi bi-columns-gap
</span>
<span>
<i class="bi bi-command"></i>
bi bi-command
</span>
<span>
<i class="bi bi-compass"></i>
bi bi-compass
</span>
<span>
<i class="bi bi-cone"></i>
bi bi-cone
</span>
<span>
<i class="bi bi-cone-striped"></i>
bi bi-cone-striped
</span>
<span>
<i class="bi bi-controller"></i>
bi bi-controller
</span>
<span>
<i class="bi bi-cookie"></i>
bi bi-cookie
</span>
<span>
<i class="bi bi-copy"></i>
bi bi-copy
</span>
<span>
<i class="bi bi-cpu"></i>
bi bi-cpu
</span>
<span>
<i class="bi bi-credit-card"></i>
bi bi-credit-card
</span>
<span>
<i class="bi bi-credit-card-2-back"></i>
bi bi-credit-card-2-back
</span>
<span>
<i class="bi bi-credit-card-2-front"></i>
bi bi-credit-card-2-front
</span>
<span>
<i class="bi bi-crop"></i>
bi bi-crop
</span>
<span>
<i class="bi bi-crosshair"></i>
bi bi-crosshair
</span>
<span>
<i class="bi bi-crosshair2"></i>
bi bi-crosshair2
</span>
<span>
<i class="bi bi-css"></i>
bi bi-css
</span>
<span>
<i class="bi bi-cup"></i>
bi bi-cup
</span>
<span>
<i class="bi bi-cup-hot"></i>
bi bi-cup-hot
</span>
<span>
<i class="bi bi-cup-straw"></i>
bi bi-cup-straw
</span>
<span>
<i class="bi bi-currency-bitcoin"></i>
bi bi-currency-bitcoin
</span>
<span>
<i class="bi bi-currency-dollar"></i>
bi bi-currency-dollar
</span>
<span>
<i class="bi bi-currency-euro"></i>
bi bi-currency-euro
</span>
<span>
<i class="bi bi-currency-exchange"></i>
bi bi-currency-exchange
</span>
<span>
<i class="bi bi-currency-pound"></i>
bi bi-currency-pound
</span>
<span>
<i class="bi bi-currency-rupee"></i>
bi bi-currency-rupee
</span>
<span>
<i class="bi bi-currency-yen"></i>
bi bi-currency-yen
</span>
<span>
<i class="bi bi-cursor"></i>
bi bi-cursor
</span>
<span>
<i class="bi bi-cursor-text"></i>
bi bi-cursor-text
</span>
<span>
<i class="bi bi-dash"></i>
bi bi-dash
</span>
<span>
<i class="bi bi-dash-circle"></i>
bi bi-dash-circle
</span>
<span>
<i class="bi bi-dash-circle-dotted"></i>
bi bi-dash-circle-dotted
</span>
<span>
<i class="bi bi-dash-lg"></i>
bi bi-dash-lg
</span>
<span>
<i class="bi bi-dash-square"></i>
bi bi-dash-square
</span>
<span>
<i class="bi bi-dash-square-dotted"></i>
bi bi-dash-square-dotted
</span>
<span>
<i class="bi bi-database"></i>
bi bi-database
</span>
<span>
<i class="bi bi-database-add"></i>
bi bi-database-add
</span>
<span>
<i class="bi bi-database-check"></i>
bi bi-database-check
</span>
<span>
<i class="bi bi-database-dash"></i>
bi bi-database-dash
</span>
<span>
<i class="bi bi-database-down"></i>
bi bi-database-down
</span>
<span>
<i class="bi bi-database-exclamation"></i>
bi bi-database-exclamation
</span>
<span>
<i class="bi bi-database-gear"></i>
bi bi-database-gear
</span>
<span>
<i class="bi bi-database-lock"></i>
bi bi-database-lock
</span>
<span>
<i class="bi bi-database-slash"></i>
bi bi-database-slash
</span>
<span>
<i class="bi bi-database-up"></i>
bi bi-database-up
</span>
<span>
<i class="bi bi-database-x"></i>
bi bi-database-x
</span>
<span>
<i class="bi bi-device-hdd"></i>
bi bi-device-hdd
</span>
<span>
<i class="bi bi-device-ssd"></i>
bi bi-device-ssd
</span>
<span>
<i class="bi bi-diagram-2"></i>
bi bi-diagram-2
</span>
<span>
<i class="bi bi-diagram-3"></i>
bi bi-diagram-3
</span>
<span>
<i class="bi bi-diamond"></i>
bi bi-diamond
</span>
<span>
<i class="bi bi-diamond-half"></i>
bi bi-diamond-half
</span>
<span>
<i class="bi bi-dice-1"></i>
bi bi-dice-1
</span>
<span>
<i class="bi bi-dice-2"></i>
bi bi-dice-2
</span>
<span>
<i class="bi bi-dice-3"></i>
bi bi-dice-3
</span>
<span>
<i class="bi bi-dice-4"></i>
bi bi-dice-4
</span>
<span>
<i class="bi bi-dice-5"></i>
bi bi-dice-5
</span>
<span>
<i class="bi bi-dice-6"></i>
bi bi-dice-6
</span>
<span>
<i class="bi bi-disc"></i>
bi bi-disc
</span>
<span>
<i class="bi bi-discord"></i>
bi bi-discord
</span>
<span>
<i class="bi bi-display"></i>
bi bi-display
</span>
<span>
<i class="bi bi-displayport"></i>
bi bi-displayport
</span>
<span>
<i class="bi bi-distribute-horizontal"></i>
bi bi-distribute-horizontal
</span>
<span>
<i class="bi bi-distribute-vertical"></i>
bi bi-distribute-vertical
</span>
<span>
<i class="bi bi-door-closed"></i>
bi bi-door-closed
</span>
<span>
<i class="bi bi-door-open"></i>
bi bi-door-open
</span>
<span>
<i class="bi bi-dot"></i>
bi bi-dot
</span>
<span>
<i class="bi bi-download"></i>
bi bi-download
</span>
<span>
<i class="bi bi-dpad"></i>
bi bi-dpad
</span>
<span>
<i class="bi bi-dribbble"></i>
bi bi-dribbble
</span>
<span>
<i class="bi bi-dropbox"></i>
bi bi-dropbox
</span>
<span>
<i class="bi bi-droplet"></i>
bi bi-droplet
</span>
<span>
<i class="bi bi-droplet-half"></i>
bi bi-droplet-half
</span>
<span>
<i class="bi bi-duffle"></i>
bi bi-duffle
</span>
<span>
<i class="bi bi-ear"></i>
bi bi-ear
</span>
<span>
<i class="bi bi-earbuds"></i>
bi bi-earbuds
</span>
<span>
<i class="bi bi-easel"></i>
bi bi-easel
</span>
<span>
<i class="bi bi-easel2"></i>
bi bi-easel2
</span>
<span>
<i class="bi bi-easel3"></i>
bi bi-easel3
</span>
<span>
<i class="bi bi-egg"></i>
bi bi-egg
</span>
<span>
<i class="bi bi-egg-fried"></i>
bi bi-egg-fried
</span>
<span>
<i class="bi bi-eject"></i>
bi bi-eject
</span>
<span>
<i class="bi bi-emoji-angry"></i>
bi bi-emoji-angry
</span>
<span>
<i class="bi bi-emoji-astonished"></i>
bi bi-emoji-astonished
</span>
<span>
<i class="bi bi-emoji-dizzy"></i>
bi bi-emoji-dizzy
</span>
<span>
<i class="bi bi-emoji-expressionless"></i>
bi bi-emoji-expressionless
</span>
<span>
<i class="bi bi-emoji-frown"></i>
bi bi-emoji-frown
</span>
<span>
<i class="bi bi-emoji-grimace"></i>
bi bi-emoji-grimace
</span>
<span>
<i class="bi bi-emoji-grin"></i>
bi bi-emoji-grin
</span>
<span>
<i class="bi bi-emoji-heart-eyes"></i>
bi bi-emoji-heart-eyes
</span>
<span>
<i class="bi bi-emoji-kiss"></i>
bi bi-emoji-kiss
</span>
<span>
<i class="bi bi-emoji-laughing"></i>
bi bi-emoji-laughing
</span>
<span>
<i class="bi bi-emoji-neutral"></i>
bi bi-emoji-neutral
</span>
<span>
<i class="bi bi-emoji-smile"></i>
bi bi-emoji-smile
</span>
<span>
<i class="bi bi-emoji-smile-upside-down"></i>
bi bi-emoji-smile-upside-down
</span>
<span>
<i class="bi bi-emoji-sunglasses"></i>
bi bi-emoji-sunglasses
</span>
<span>
<i class="bi bi-emoji-surprise"></i>
bi bi-emoji-surprise
</span>
<span>
<i class="bi bi-emoji-tear"></i>
bi bi-emoji-tear
</span>
<span>
<i class="bi bi-emoji-wink"></i>
bi bi-emoji-wink
</span>
<span>
<i class="bi bi-envelope"></i>
bi bi-envelope
</span>
<span>
<i class="bi bi-envelope-arrow-down"></i>
bi bi-envelope-arrow-down
</span>
<span>
<i class="bi bi-envelope-arrow-up"></i>
bi bi-envelope-arrow-up
</span>
<span>
<i class="bi bi-envelope-at"></i>
bi bi-envelope-at
</span>
<span>
<i class="bi bi-envelope-check"></i>
bi bi-envelope-check
</span>
<span>
<i class="bi bi-envelope-dash"></i>
bi bi-envelope-dash
</span>
<span>
<i class="bi bi-envelope-exclamation"></i>
bi bi-envelope-exclamation
</span>
<span>
<i class="bi bi-envelope-heart"></i>
bi bi-envelope-heart
</span>
<span>
<i class="bi bi-envelope-open"></i>
bi bi-envelope-open
</span>
<span>
<i class="bi bi-envelope-open-heart"></i>
bi bi-envelope-open-heart
</span>
<span>
<i class="bi bi-envelope-paper"></i>
bi bi-envelope-paper
</span>
<span>
<i class="bi bi-envelope-paper-heart"></i>
bi bi-envelope-paper-heart
</span>
<span>
<i class="bi bi-envelope-plus"></i>
bi bi-envelope-plus
</span>
<span>
<i class="bi bi-envelope-slash"></i>
bi bi-envelope-slash
</span>
<span>
<i class="bi bi-envelope-x"></i>
bi bi-envelope-x
</span>
<span>
<i class="bi bi-eraser"></i>
bi bi-eraser
</span>
<span>
<i class="bi bi-escape"></i>
bi bi-escape
</span>
<span>
<i class="bi bi-ethernet"></i>
bi bi-ethernet
</span>
<span>
<i class="bi bi-ev-front"></i>
bi bi-ev-front
</span>
<span>
<i class="bi bi-ev-station"></i>
bi bi-ev-station
</span>
<span>
<i class="bi bi-exclamation"></i>
bi bi-exclamation
</span>
<span>
<i class="bi bi-exclamation-circle"></i>
bi bi-exclamation-circle
</span>
<span>
<i class="bi bi-exclamation-diamond"></i>
bi bi-exclamation-diamond
</span>
<span>
<i class="bi bi-exclamation-lg"></i>
bi bi-exclamation-lg
</span>
<span>
<i class="bi bi-exclamation-octagon"></i>
bi bi-exclamation-octagon
</span>
<span>
<i class="bi bi-exclamation-square"></i>
bi bi-exclamation-square
</span>
<span>
<i class="bi bi-exclamation-triangle"></i>
bi bi-exclamation-triangle
</span>
<span>
<i class="bi bi-exclude"></i>
bi bi-exclude
</span>
<span>
<i class="bi bi-explicit"></i>
bi bi-explicit
</span>
<span>
<i class="bi bi-exposure"></i>
bi bi-exposure
</span>
<span>
<i class="bi bi-eye"></i>
bi bi-eye
</span>
<span>
<i class="bi bi-eye-slash"></i>
bi bi-eye-slash
</span>
<span>
<i class="bi bi-eyedropper"></i>
bi bi-eyedropper
</span>
<span>
<i class="bi bi-eyeglasses"></i>
bi bi-eyeglasses
</span>
<span>
<i class="bi bi-facebook"></i>
bi bi-facebook
</span>
<span>
<i class="bi bi-fan"></i>
bi bi-fan
</span>
<span>
<i class="bi bi-fast-forward"></i>
bi bi-fast-forward
</span>
<span>
<i class="bi bi-fast-forward-btn"></i>
bi bi-fast-forward-btn
</span>
<span>
<i class="bi bi-fast-forward-circle"></i>
bi bi-fast-forward-circle
</span>
<span>
<i class="bi bi-feather"></i>
bi bi-feather
</span>
<span>
<i class="bi bi-feather2"></i>
bi bi-feather2
</span>
<span>
<i class="bi bi-file"></i>
bi bi-file
</span>
<span>
<i class="bi bi-file-arrow-down"></i>
bi bi-file-arrow-down
</span>
<span>
<i class="bi bi-file-arrow-up"></i>
bi bi-file-arrow-up
</span>
<span>
<i class="bi bi-file-bar-graph"></i>
bi bi-file-bar-graph
</span>
<span>
<i class="bi bi-file-binary"></i>
bi bi-file-binary
</span>
<span>
<i class="bi bi-file-break"></i>
bi bi-file-break
</span>
<span>
<i class="bi bi-file-check"></i>
bi bi-file-check
</span>
<span>
<i class="bi bi-file-code"></i>
bi bi-file-code
</span>
<span>
<i class="bi bi-file-diff"></i>
bi bi-file-diff
</span>
<span>
<i class="bi bi-file-earmark"></i>
bi bi-file-earmark
</span>
<span>
<i class="bi bi-file-earmark-arrow-down"></i>
bi bi-file-earmark-arrow-down
</span>
<span>
<i class="bi bi-file-earmark-arrow-up"></i>
bi bi-file-earmark-arrow-up
</span>
<span>
<i class="bi bi-file-earmark-bar-graph"></i>
bi bi-file-earmark-bar-graph
</span>
<span>
<i class="bi bi-file-earmark-binary"></i>
bi bi-file-earmark-binary
</span>
<span>
<i class="bi bi-file-earmark-break"></i>
bi bi-file-earmark-break
</span>
<span>
<i class="bi bi-file-earmark-check"></i>
bi bi-file-earmark-check
</span>
<span>
<i class="bi bi-file-earmark-code"></i>
bi bi-file-earmark-code
</span>
<span>
<i class="bi bi-file-earmark-diff"></i>
bi bi-file-earmark-diff
</span>
<span>
<i class="bi bi-file-earmark-easel"></i>
bi bi-file-earmark-easel
</span>
<span>
<i class="bi bi-file-earmark-excel"></i>
bi bi-file-earmark-excel
</span>
<span>
<i class="bi bi-file-earmark-font"></i>
bi bi-file-earmark-font
</span>
<span>
<i class="bi bi-file-earmark-image"></i>
bi bi-file-earmark-image
</span>
<span>
<i class="bi bi-file-earmark-lock"></i>
bi bi-file-earmark-lock
</span>
<span>
<i class="bi bi-file-earmark-lock2"></i>
bi bi-file-earmark-lock2
</span>
<span>
<i class="bi bi-file-earmark-medical"></i>
bi bi-file-earmark-medical
</span>
<span>
<i class="bi bi-file-earmark-minus"></i>
bi bi-file-earmark-minus
</span>
<span>
<i class="bi bi-file-earmark-music"></i>
bi bi-file-earmark-music
</span>
<span>
<i class="bi bi-file-earmark-pdf"></i>
bi bi-file-earmark-pdf
</span>
<span>
<i class="bi bi-file-earmark-person"></i>
bi bi-file-earmark-person
</span>
<span>
<i class="bi bi-file-earmark-play"></i>
bi bi-file-earmark-play
</span>
<span>
<i class="bi bi-file-earmark-plus"></i>
bi bi-file-earmark-plus
</span>
<span>
<i class="bi bi-file-earmark-post"></i>
bi bi-file-earmark-post
</span>
<span>
<i class="bi bi-file-earmark-ppt"></i>
bi bi-file-earmark-ppt
</span>
<span>
<i class="bi bi-file-earmark-richtext"></i>
bi bi-file-earmark-richtext
</span>
<span>
<i class="bi bi-file-earmark-ruled"></i>
bi bi-file-earmark-ruled
</span>
<span>
<i class="bi bi-file-earmark-slides"></i>
bi bi-file-earmark-slides
</span>
<span>
<i class="bi bi-file-earmark-spreadsheet"></i>
bi bi-file-earmark-spreadsheet
</span>
<span>
<i class="bi bi-file-earmark-text"></i>
bi bi-file-earmark-text
</span>
<span>
<i class="bi bi-file-earmark-word"></i>
bi bi-file-earmark-word
</span>
<span>
<i class="bi bi-file-earmark-x"></i>
bi bi-file-earmark-x
</span>
<span>
<i class="bi bi-file-earmark-zip"></i>
bi bi-file-earmark-zip
</span>
<span>
<i class="bi bi-file-easel"></i>
bi bi-file-easel
</span>
<span>
<i class="bi bi-file-excel"></i>
bi bi-file-excel
</span>
<span>
<i class="bi bi-file-font"></i>
bi bi-file-font
</span>
<span>
<i class="bi bi-file-image"></i>
bi bi-file-image
</span>
<span>
<i class="bi bi-file-lock"></i>
bi bi-file-lock
</span>
<span>
<i class="bi bi-file-lock2"></i>
bi bi-file-lock2
</span>
<span>
<i class="bi bi-file-medical"></i>
bi bi-file-medical
</span>
<span>
<i class="bi bi-file-minus"></i>
bi bi-file-minus
</span>
<span>
<i class="bi bi-file-music"></i>
bi bi-file-music
</span>
<span>
<i class="bi bi-file-pdf"></i>
bi bi-file-pdf
</span>
<span>
<i class="bi bi-file-person"></i>
bi bi-file-person
</span>
<span>
<i class="bi bi-file-play"></i>
bi bi-file-play
</span>
<span>
<i class="bi bi-file-plus"></i>
bi bi-file-plus
</span>
<span>
<i class="bi bi-file-post"></i>
bi bi-file-post
</span>
<span>
<i class="bi bi-file-ppt"></i>
bi bi-file-ppt
</span>
<span>
<i class="bi bi-file-richtext"></i>
bi bi-file-richtext
</span>
<span>
<i class="bi bi-file-ruled"></i>
bi bi-file-ruled
</span>
<span>
<i class="bi bi-file-slides"></i>
bi bi-file-slides
</span>
<span>
<i class="bi bi-file-spreadsheet"></i>
bi bi-file-spreadsheet
</span>
<span>
<i class="bi bi-file-text"></i>
bi bi-file-text
</span>
<span>
<i class="bi bi-file-word"></i>
bi bi-file-word
</span>
<span>
<i class="bi bi-file-x"></i>
bi bi-file-x
</span>
<span>
<i class="bi bi-file-zip"></i>
bi bi-file-zip
</span>
<span>
<i class="bi bi-files"></i>
bi bi-files
</span>
<span>
<i class="bi bi-files-alt"></i>
bi bi-files-alt
</span>
<span>
<i class="bi bi-filetype-aac"></i>
bi bi-filetype-aac
</span>
<span>
<i class="bi bi-filetype-ai"></i>
bi bi-filetype-ai
</span>
<span>
<i class="bi bi-filetype-bmp"></i>
bi bi-filetype-bmp
</span>
<span>
<i class="bi bi-filetype-cs"></i>
bi bi-filetype-cs
</span>
<span>
<i class="bi bi-filetype-css"></i>
bi bi-filetype-css
</span>
<span>
<i class="bi bi-filetype-csv"></i>
bi bi-filetype-csv
</span>
<span>
<i class="bi bi-filetype-doc"></i>
bi bi-filetype-doc
</span>
<span>
<i class="bi bi-filetype-docx"></i>
bi bi-filetype-docx
</span>
<span>
<i class="bi bi-filetype-exe"></i>
bi bi-filetype-exe
</span>
<span>
<i class="bi bi-filetype-gif"></i>
bi bi-filetype-gif
</span>
<span>
<i class="bi bi-filetype-heic"></i>
bi bi-filetype-heic
</span>
<span>
<i class="bi bi-filetype-html"></i>
bi bi-filetype-html
</span>
<span>
<i class="bi bi-filetype-java"></i>
bi bi-filetype-java
</span>
<span>
<i class="bi bi-filetype-jpg"></i>
bi bi-filetype-jpg
</span>
<span>
<i class="bi bi-filetype-js"></i>
bi bi-filetype-js
</span>
<span>
<i class="bi bi-filetype-json"></i>
bi bi-filetype-json
</span>
<span>
<i class="bi bi-filetype-jsx"></i>
bi bi-filetype-jsx
</span>
<span>
<i class="bi bi-filetype-key"></i>
bi bi-filetype-key
</span>
<span>
<i class="bi bi-filetype-m4p"></i>
bi bi-filetype-m4p
</span>
<span>
<i class="bi bi-filetype-md"></i>
bi bi-filetype-md
</span>
<span>
<i class="bi bi-filetype-mdx"></i>
bi bi-filetype-mdx
</span>
<span>
<i class="bi bi-filetype-mov"></i>
bi bi-filetype-mov
</span>
<span>
<i class="bi bi-filetype-mp3"></i>
bi bi-filetype-mp3
</span>
<span>
<i class="bi bi-filetype-mp4"></i>
bi bi-filetype-mp4
</span>
<span>
<i class="bi bi-filetype-otf"></i>
bi bi-filetype-otf
</span>
<span>
<i class="bi bi-filetype-pdf"></i>
bi bi-filetype-pdf
</span>
<span>
<i class="bi bi-filetype-php"></i>
bi bi-filetype-php
</span>
<span>
<i class="bi bi-filetype-png"></i>
bi bi-filetype-png
</span>
<span>
<i class="bi bi-filetype-ppt"></i>
bi bi-filetype-ppt
</span>
<span>
<i class="bi bi-filetype-pptx"></i>
bi bi-filetype-pptx
</span>
<span>
<i class="bi bi-filetype-psd"></i>
bi bi-filetype-psd
</span>
<span>
<i class="bi bi-filetype-py"></i>
bi bi-filetype-py
</span>
<span>
<i class="bi bi-filetype-raw"></i>
bi bi-filetype-raw
</span>
<span>
<i class="bi bi-filetype-rb"></i>
bi bi-filetype-rb
</span>
<span>
<i class="bi bi-filetype-sass"></i>
bi bi-filetype-sass
</span>
<span>
<i class="bi bi-filetype-scss"></i>
bi bi-filetype-scss
</span>
<span>
<i class="bi bi-filetype-sh"></i>
bi bi-filetype-sh
</span>
<span>
<i class="bi bi-filetype-sql"></i>
bi bi-filetype-sql
</span>
<span>
<i class="bi bi-filetype-svg"></i>
bi bi-filetype-svg
</span>
<span>
<i class="bi bi-filetype-tiff"></i>
bi bi-filetype-tiff
</span>
<span>
<i class="bi bi-filetype-tsx"></i>
bi bi-filetype-tsx
</span>
<span>
<i class="bi bi-filetype-ttf"></i>
bi bi-filetype-ttf
</span>
<span>
<i class="bi bi-filetype-txt"></i>
bi bi-filetype-txt
</span>
<span>
<i class="bi bi-filetype-wav"></i>
bi bi-filetype-wav
</span>
<span>
<i class="bi bi-filetype-woff"></i>
bi bi-filetype-woff
</span>
<span>
<i class="bi bi-filetype-xls"></i>
bi bi-filetype-xls
</span>
<span>
<i class="bi bi-filetype-xlsx"></i>
bi bi-filetype-xlsx
</span>
<span>
<i class="bi bi-filetype-xml"></i>
bi bi-filetype-xml
</span>
<span>
<i class="bi bi-filetype-yml"></i>
bi bi-filetype-yml
</span>
<span>
<i class="bi bi-film"></i>
bi bi-film
</span>
<span>
<i class="bi bi-filter"></i>
bi bi-filter
</span>
<span>
<i class="bi bi-filter-circle"></i>
bi bi-filter-circle
</span>
<span>
<i class="bi bi-filter-left"></i>
bi bi-filter-left
</span>
<span>
<i class="bi bi-filter-right"></i>
bi bi-filter-right
</span>
<span>
<i class="bi bi-filter-square"></i>
bi bi-filter-square
</span>
<span>
<i class="bi bi-fingerprint"></i>
bi bi-fingerprint
</span>
<span>
<i class="bi bi-fire"></i>
bi bi-fire
</span>
<span>
<i class="bi bi-flag"></i>
bi bi-flag
</span>
<span>
<i class="bi bi-flask"></i>
bi bi-flask
</span>
<span>
<i class="bi bi-flask-florence"></i>
bi bi-flask-florence
</span>
<span>
<i class="bi bi-floppy"></i>
bi bi-floppy
</span>
<span>
<i class="bi bi-floppy2"></i>
bi bi-floppy2
</span>
<span>
<i class="bi bi-flower1"></i>
bi bi-flower1
</span>
<span>
<i class="bi bi-flower2"></i>
bi bi-flower2
</span>
<span>
<i class="bi bi-flower3"></i>
bi bi-flower3
</span>
<span>
<i class="bi bi-folder"></i>
bi bi-folder
</span>
<span>
<i class="bi bi-folder-check"></i>
bi bi-folder-check
</span>
<span>
<i class="bi bi-folder-minus"></i>
bi bi-folder-minus
</span>
<span>
<i class="bi bi-folder-plus"></i>
bi bi-folder-plus
</span>
<span>
<i class="bi bi-folder-symlink"></i>
bi bi-folder-symlink
</span>
<span>
<i class="bi bi-folder-x"></i>
bi bi-folder-x
</span>
<span>
<i class="bi bi-folder2"></i>
bi bi-folder2
</span>
<span>
<i class="bi bi-folder2-open"></i>
bi bi-folder2-open
</span>
<span>
<i class="bi bi-fonts"></i>
bi bi-fonts
</span>
<span>
<i class="bi bi-fork-knife"></i>
bi bi-fork-knife
</span>
<span>
<i class="bi bi-forward"></i>
bi bi-forward
</span>
<span>
<i class="bi bi-front"></i>
bi bi-front
</span>
<span>
<i class="bi bi-fuel-pump"></i>
bi bi-fuel-pump
</span>
<span>
<i class="bi bi-fuel-pump-diesel"></i>
bi bi-fuel-pump-diesel
</span>
<span>
<i class="bi bi-fullscreen"></i>
bi bi-fullscreen
</span>
<span>
<i class="bi bi-fullscreen-exit"></i>
bi bi-fullscreen-exit
</span>
<span>
<i class="bi bi-funnel"></i>
bi bi-funnel
</span>
<span>
<i class="bi bi-gear"></i>
bi bi-gear
</span>
<span>
<i class="bi bi-gear-wide"></i>
bi bi-gear-wide
</span>
<span>
<i class="bi bi-gear-wide-connected"></i>
bi bi-gear-wide-connected
</span>
<span>
<i class="bi bi-gem"></i>
bi bi-gem
</span>
<span>
<i class="bi bi-gender-ambiguous"></i>
bi bi-gender-ambiguous
</span>
<span>
<i class="bi bi-gender-female"></i>
bi bi-gender-female
</span>
<span>
<i class="bi bi-gender-male"></i>
bi bi-gender-male
</span>
<span>
<i class="bi bi-gender-neuter"></i>
bi bi-gender-neuter
</span>
<span>
<i class="bi bi-gender-trans"></i>
bi bi-gender-trans
</span>
<span>
<i class="bi bi-geo"></i>
bi bi-geo
</span>
<span>
<i class="bi bi-geo-alt"></i>
bi bi-geo-alt
</span>
<span>
<i class="bi bi-gift"></i>
bi bi-gift
</span>
<span>
<i class="bi bi-git"></i>
bi bi-git
</span>
<span>
<i class="bi bi-github"></i>
bi bi-github
</span>
<span>
<i class="bi bi-gitlab"></i>
bi bi-gitlab
</span>
<span>
<i class="bi bi-globe"></i>
bi bi-globe
</span>
<span>
<i class="bi bi-globe-americas"></i>
bi bi-globe-americas
</span>
<span>
<i class="bi bi-globe-asia-australia"></i>
bi bi-globe-asia-australia
</span>
<span>
<i class="bi bi-globe-central-south-asia"></i>
bi bi-globe-central-south-asia
</span>
<span>
<i class="bi bi-globe-europe-africa"></i>
bi bi-globe-europe-africa
</span>
<span>
<i class="bi bi-globe2"></i>
bi bi-globe2
</span>
<span>
<i class="bi bi-google"></i>
bi bi-google
</span>
<span>
<i class="bi bi-google-play"></i>
bi bi-google-play
</span>
<span>
<i class="bi bi-gpu-card"></i>
bi bi-gpu-card
</span>
<span>
<i class="bi bi-graph-down"></i>
bi bi-graph-down
</span>
<span>
<i class="bi bi-graph-down-arrow"></i>
bi bi-graph-down-arrow
</span>
<span>
<i class="bi bi-graph-up"></i>
bi bi-graph-up
</span>
<span>
<i class="bi bi-graph-up-arrow"></i>
bi bi-graph-up-arrow
</span>
<span>
<i class="bi bi-grid"></i>
bi bi-grid
</span>
<span>
<i class="bi bi-grid-1x2"></i>
bi bi-grid-1x2
</span>
<span>
<i class="bi bi-grid-3x2"></i>
bi bi-grid-3x2
</span>
<span>
<i class="bi bi-grid-3x2-gap"></i>
bi bi-grid-3x2-gap
</span>
<span>
<i class="bi bi-grid-3x3"></i>
bi bi-grid-3x3
</span>
<span>
<i class="bi bi-grid-3x3-gap"></i>
bi bi-grid-3x3-gap
</span>
<span>
<i class="bi bi-grip-horizontal"></i>
bi bi-grip-horizontal
</span>
<span>
<i class="bi bi-grip-vertical"></i>
bi bi-grip-vertical
</span>
<span>
<i class="bi bi-h-circle"></i>
bi bi-h-circle
</span>
<span>
<i class="bi bi-h-square"></i>
bi bi-h-square
</span>
<span>
<i class="bi bi-hammer"></i>
bi bi-hammer
</span>
<span>
<i class="bi bi-hand-index"></i>
bi bi-hand-index
</span>
<span>
<i class="bi bi-hand-index-thumb"></i>
bi bi-hand-index-thumb
</span>
<span>
<i class="bi bi-hand-thumbs-down"></i>
bi bi-hand-thumbs-down
</span>
<span>
<i class="bi bi-hand-thumbs-up"></i>
bi bi-hand-thumbs-up
</span>
<span>
<i class="bi bi-handbag"></i>
bi bi-handbag
</span>
<span>
<i class="bi bi-hash"></i>
bi bi-hash
</span>
<span>
<i class="bi bi-hdd"></i>
bi bi-hdd
</span>
<span>
<i class="bi bi-hdd-network"></i>
bi bi-hdd-network
</span>
<span>
<i class="bi bi-hdd-rack"></i>
bi bi-hdd-rack
</span>
<span>
<i class="bi bi-hdd-stack"></i>
bi bi-hdd-stack
</span>
<span>
<i class="bi bi-hdmi"></i>
bi bi-hdmi
</span>
<span>
<i class="bi bi-headphones"></i>
bi bi-headphones
</span>
<span>
<i class="bi bi-headset"></i>
bi bi-headset
</span>
<span>
<i class="bi bi-headset-vr"></i>
bi bi-headset-vr
</span>
<span>
<i class="bi bi-heart"></i>
bi bi-heart
</span>
<span>
<i class="bi bi-heart-arrow"></i>
bi bi-heart-arrow
</span>
<span>
<i class="bi bi-heart-half"></i>
bi bi-heart-half
</span>
<span>
<i class="bi bi-heart-pulse"></i>
bi bi-heart-pulse
</span>
<span>
<i class="bi bi-heartbreak"></i>
bi bi-heartbreak
</span>
<span>
<i class="bi bi-hearts"></i>
bi bi-hearts
</span>
<span>
<i class="bi bi-heptagon"></i>
bi bi-heptagon
</span>
<span>
<i class="bi bi-heptagon-half"></i>
bi bi-heptagon-half
</span>
<span>
<i class="bi bi-hexagon"></i>
bi bi-hexagon
</span>
<span>
<i class="bi bi-hexagon-half"></i>
bi bi-hexagon-half
</span>
<span>
<i class="bi bi-highlighter"></i>
bi bi-highlighter
</span>
<span>
<i class="bi bi-highlights"></i>
bi bi-highlights
</span>
<span>
<i class="bi bi-hospital"></i>
bi bi-hospital
</span>
<span>
<i class="bi bi-hourglass"></i>
bi bi-hourglass
</span>
<span>
<i class="bi bi-hourglass-bottom"></i>
bi bi-hourglass-bottom
</span>
<span>
<i class="bi bi-hourglass-split"></i>
bi bi-hourglass-split
</span>
<span>
<i class="bi bi-hourglass-top"></i>
bi bi-hourglass-top
</span>
<span>
<i class="bi bi-house"></i>
bi bi-house
</span>
<span>
<i class="bi bi-house-add"></i>
bi bi-house-add
</span>
<span>
<i class="bi bi-house-check"></i>
bi bi-house-check
</span>
<span>
<i class="bi bi-house-dash"></i>
bi bi-house-dash
</span>
<span>
<i class="bi bi-house-door"></i>
bi bi-house-door
</span>
<span>
<i class="bi bi-house-down"></i>
bi bi-house-down
</span>
<span>
<i class="bi bi-house-exclamation"></i>
bi bi-house-exclamation
</span>
<span>
<i class="bi bi-house-gear"></i>
bi bi-house-gear
</span>
<span>
<i class="bi bi-house-heart"></i>
bi bi-house-heart
</span>
<span>
<i class="bi bi-house-lock"></i>
bi bi-house-lock
</span>
<span>
<i class="bi bi-house-slash"></i>
bi bi-house-slash
</span>
<span>
<i class="bi bi-house-up"></i>
bi bi-house-up
</span>
<span>
<i class="bi bi-house-x"></i>
bi bi-house-x
</span>
<span>
<i class="bi bi-houses"></i>
bi bi-houses
</span>
<span>
<i class="bi bi-hr"></i>
bi bi-hr
</span>
<span>
<i class="bi bi-hurricane"></i>
bi bi-hurricane
</span>
<span>
<i class="bi bi-hypnotize"></i>
bi bi-hypnotize
</span>
<span>
<i class="bi bi-image"></i>
bi bi-image
</span>
<span>
<i class="bi bi-image-alt"></i>
bi bi-image-alt
</span>
<span>
<i class="bi bi-images"></i>
bi bi-images
</span>
<span>
<i class="bi bi-inbox"></i>
bi bi-inbox
</span>
<span>
<i class="bi bi-inboxes"></i>
bi bi-inboxes
</span>
<span>
<i class="bi bi-incognito"></i>
bi bi-incognito
</span>
<span>
<i class="bi bi-indent"></i>
bi bi-indent
</span>
<span>
<i class="bi bi-infinity"></i>
bi bi-infinity
</span>
<span>
<i class="bi bi-info"></i>
bi bi-info
</span>
<span>
<i class="bi bi-info-circle"></i>
bi bi-info-circle
</span>
<span>
<i class="bi bi-info-lg"></i>
bi bi-info-lg
</span>
<span>
<i class="bi bi-info-square"></i>
bi bi-info-square
</span>
<span>
<i class="bi bi-input-cursor"></i>
bi bi-input-cursor
</span>
<span>
<i class="bi bi-input-cursor-text"></i>
bi bi-input-cursor-text
</span>
<span>
<i class="bi bi-instagram"></i>
bi bi-instagram
</span>
<span>
<i class="bi bi-intersect"></i>
bi bi-intersect
</span>
<span>
<i class="bi bi-javascript"></i>
bi bi-javascript
</span>
<span>
<i class="bi bi-journal"></i>
bi bi-journal
</span>
<span>
<i class="bi bi-journal-album"></i>
bi bi-journal-album
</span>
<span>
<i class="bi bi-journal-arrow-down"></i>
bi bi-journal-arrow-down
</span>
<span>
<i class="bi bi-journal-arrow-up"></i>
bi bi-journal-arrow-up
</span>
<span>
<i class="bi bi-journal-bookmark"></i>
bi bi-journal-bookmark
</span>
<span>
<i class="bi bi-journal-check"></i>
bi bi-journal-check
</span>
<span>
<i class="bi bi-journal-code"></i>
bi bi-journal-code
</span>
<span>
<i class="bi bi-journal-medical"></i>
bi bi-journal-medical
</span>
<span>
<i class="bi bi-journal-minus"></i>
bi bi-journal-minus
</span>
<span>
<i class="bi bi-journal-plus"></i>
bi bi-journal-plus
</span>
<span>
<i class="bi bi-journal-richtext"></i>
bi bi-journal-richtext
</span>
<span>
<i class="bi bi-journal-text"></i>
bi bi-journal-text
</span>
<span>
<i class="bi bi-journal-x"></i>
bi bi-journal-x
</span>
<span>
<i class="bi bi-journals"></i>
bi bi-journals
</span>
<span>
<i class="bi bi-joystick"></i>
bi bi-joystick
</span>
<span>
<i class="bi bi-justify"></i>
bi bi-justify
</span>
<span>
<i class="bi bi-justify-left"></i>
bi bi-justify-left
</span>
<span>
<i class="bi bi-justify-right"></i>
bi bi-justify-right
</span>
<span>
<i class="bi bi-kanban"></i>
bi bi-kanban
</span>
<span>
<i class="bi bi-key"></i>
bi bi-key
</span>
<span>
<i class="bi bi-keyboard"></i>
bi bi-keyboard
</span>
<span>
<i class="bi bi-ladder"></i>
bi bi-ladder
</span>
<span>
<i class="bi bi-lamp"></i>
bi bi-lamp
</span>
<span>
<i class="bi bi-laptop"></i>
bi bi-laptop
</span>
<span>
<i class="bi bi-layer-backward"></i>
bi bi-layer-backward
</span>
<span>
<i class="bi bi-layer-forward"></i>
bi bi-layer-forward
</span>
<span>
<i class="bi bi-layers"></i>
bi bi-layers
</span>
<span>
<i class="bi bi-layers-half"></i>
bi bi-layers-half
</span>
<span>
<i class="bi bi-layout-sidebar"></i>
bi bi-layout-sidebar
</span>
<span>
<i class="bi bi-layout-sidebar-inset-reverse"></i>
bi bi-layout-sidebar-inset-reverse
</span>
<span>
<i class="bi bi-layout-sidebar-inset"></i>
bi bi-layout-sidebar-inset
</span>
<span>
<i class="bi bi-layout-sidebar-reverse"></i>
bi bi-layout-sidebar-reverse
</span>
<span>
<i class="bi bi-layout-split"></i>
bi bi-layout-split
</span>
<span>
<i class="bi bi-layout-text-sidebar"></i>
bi bi-layout-text-sidebar
</span>
<span>
<i class="bi bi-layout-text-sidebar-reverse"></i>
bi bi-layout-text-sidebar-reverse
</span>
<span>
<i class="bi bi-layout-text-window"></i>
bi bi-layout-text-window
</span>
<span>
<i class="bi bi-layout-text-window-reverse"></i>
bi bi-layout-text-window-reverse
</span>
<span>
<i class="bi bi-layout-three-columns"></i>
bi bi-layout-three-columns
</span>
<span>
<i class="bi bi-layout-wtf"></i>
bi bi-layout-wtf
</span>
<span>
<i class="bi bi-leaf"></i>
bi bi-leaf
</span>
<span>
<i class="bi bi-life-preserver"></i>
bi bi-life-preserver
</span>
<span>
<i class="bi bi-lightbulb"></i>
bi bi-lightbulb
</span>
<span>
<i class="bi bi-lightbulb-off"></i>
bi bi-lightbulb-off
</span>
<span>
<i class="bi bi-lightning"></i>
bi bi-lightning
</span>
<span>
<i class="bi bi-lightning-charge"></i>
bi bi-lightning-charge
</span>
<span>
<i class="bi bi-line"></i>
bi bi-line
</span>
<span>
<i class="bi bi-link"></i>
bi bi-link
</span>
<span>
<i class="bi bi-link-45deg"></i>
bi bi-link-45deg
</span>
<span>
<i class="bi bi-linkedin"></i>
bi bi-linkedin
</span>
<span>
<i class="bi bi-list"></i>
bi bi-list
</span>
<span>
<i class="bi bi-list-check"></i>
bi bi-list-check
</span>
<span>
<i class="bi bi-list-columns"></i>
bi bi-list-columns
</span>
<span>
<i class="bi bi-list-columns-reverse"></i>
bi bi-list-columns-reverse
</span>
<span>
<i class="bi bi-list-nested"></i>
bi bi-list-nested
</span>
<span>
<i class="bi bi-list-ol"></i>
bi bi-list-ol
</span>
<span>
<i class="bi bi-list-stars"></i>
bi bi-list-stars
</span>
<span>
<i class="bi bi-list-task"></i>
bi bi-list-task
</span>
<span>
<i class="bi bi-list-ul"></i>
bi bi-list-ul
</span>
<span>
<i class="bi bi-lock"></i>
bi bi-lock
</span>
<span>
<i class="bi bi-luggage"></i>
bi bi-luggage
</span>
<span>
<i class="bi bi-lungs"></i>
bi bi-lungs
</span>
<span>
<i class="bi bi-magic"></i>
bi bi-magic
</span>
<span>
<i class="bi bi-magnet"></i>
bi bi-magnet
</span>
<span>
<i class="bi bi-mailbox"></i>
bi bi-mailbox
</span>
<span>
<i class="bi bi-mailbox-flag"></i>
bi bi-mailbox-flag
</span>
<span>
<i class="bi bi-mailbox2"></i>
bi bi-mailbox2
</span>
<span>
<i class="bi bi-mailbox2-flag"></i>
bi bi-mailbox2-flag
</span>
<span>
<i class="bi bi-map"></i>
bi bi-map
</span>
<span>
<i class="bi bi-markdown"></i>
bi bi-markdown
</span>
<span>
<i class="bi bi-marker-tip"></i>
bi bi-marker-tip
</span>
<span>
<i class="bi bi-mask"></i>
bi bi-mask
</span>
<span>
<i class="bi bi-mastodon"></i>
bi bi-mastodon
</span>
<span>
<i class="bi bi-measuring-cup"></i>
bi bi-measuring-cup
</span>
<span>
<i class="bi bi-medium"></i>
bi bi-medium
</span>
<span>
<i class="bi bi-megaphone"></i>
bi bi-megaphone
</span>
<span>
<i class="bi bi-memory"></i>
bi bi-memory
</span>
<span>
<i class="bi bi-menu-app"></i>
bi bi-menu-app
</span>
<span>
<i class="bi bi-menu-button"></i>
bi bi-menu-button
</span>
<span>
<i class="bi bi-menu-button-wide"></i>
bi bi-menu-button-wide
</span>
<span>
<i class="bi bi-menu-down"></i>
bi bi-menu-down
</span>
<span>
<i class="bi bi-menu-up"></i>
bi bi-menu-up
</span>
<span>
<i class="bi bi-messenger"></i>
bi bi-messenger
</span>
<span>
<i class="bi bi-meta"></i>
bi bi-meta
</span>
<span>
<i class="bi bi-mic"></i>
bi bi-mic
</span>
<span>
<i class="bi bi-mic-mute"></i>
bi bi-mic-mute
</span>
<span>
<i class="bi bi-microsoft"></i>
bi bi-microsoft
</span>
<span>
<i class="bi bi-microsoft-teams"></i>
bi bi-microsoft-teams
</span>
<span>
<i class="bi bi-minecart"></i>
bi bi-minecart
</span>
<span>
<i class="bi bi-minecart-loaded"></i>
bi bi-minecart-loaded
</span>
<span>
<i class="bi bi-modem"></i>
bi bi-modem
</span>
<span>
<i class="bi bi-moisture"></i>
bi bi-moisture
</span>
<span>
<i class="bi bi-moon"></i>
bi bi-moon
</span>
<span>
<i class="bi bi-moon-stars"></i>
bi bi-moon-stars
</span>
<span>
<i class="bi bi-mortarboard"></i>
bi bi-mortarboard
</span>
<span>
<i class="bi bi-motherboard"></i>
bi bi-motherboard
</span>
<span>
<i class="bi bi-mouse"></i>
bi bi-mouse
</span>
<span>
<i class="bi bi-mouse2"></i>
bi bi-mouse2
</span>
<span>
<i class="bi bi-mouse3"></i>
bi bi-mouse3
</span>
<span>
<i class="bi bi-music-note"></i>
bi bi-music-note
</span>
<span>
<i class="bi bi-music-note-beamed"></i>
bi bi-music-note-beamed
</span>
<span>
<i class="bi bi-music-note-list"></i>
bi bi-music-note-list
</span>
<span>
<i class="bi bi-music-player"></i>
bi bi-music-player
</span>
<span>
<i class="bi bi-newspaper"></i>
bi bi-newspaper
</span>
<span>
<i class="bi bi-nintendo-switch"></i>
bi bi-nintendo-switch
</span>
<span>
<i class="bi bi-node-minus"></i>
bi bi-node-minus
</span>
<span>
<i class="bi bi-node-plus"></i>
bi bi-node-plus
</span>
<span>
<i class="bi bi-noise-reduction"></i>
bi bi-noise-reduction
</span>
<span>
<i class="bi bi-nut"></i>
bi bi-nut
</span>
<span>
<i class="bi bi-nvidia"></i>
bi bi-nvidia
</span>
<span>
<i class="bi bi-nvme"></i>
bi bi-nvme
</span>
<span>
<i class="bi bi-octagon"></i>
bi bi-octagon
</span>
<span>
<i class="bi bi-octagon-half"></i>
bi bi-octagon-half
</span>
<span>
<i class="bi bi-openai"></i>
bi bi-openai
</span>
<span>
<i class="bi bi-opencollective"></i>
bi bi-opencollective
</span>
<span>
<i class="bi bi-optical-audio"></i>
bi bi-optical-audio
</span>
<span>
<i class="bi bi-option"></i>
bi bi-option
</span>
<span>
<i class="bi bi-outlet"></i>
bi bi-outlet
</span>
<span>
<i class="bi bi-p-circle"></i>
bi bi-p-circle
</span>
<span>
<i class="bi bi-p-square"></i>
bi bi-p-square
</span>
<span>
<i class="bi bi-paint-bucket"></i>
bi bi-paint-bucket
</span>
<span>
<i class="bi bi-palette"></i>
bi bi-palette
</span>
<span>
<i class="bi bi-palette2"></i>
bi bi-palette2
</span>
<span>
<i class="bi bi-paperclip"></i>
bi bi-paperclip
</span>
<span>
<i class="bi bi-paragraph"></i>
bi bi-paragraph
</span>
<span>
<i class="bi bi-pass"></i>
bi bi-pass
</span>
<span>
<i class="bi bi-passport"></i>
bi bi-passport
</span>
<span>
<i class="bi bi-patch-check"></i>
bi bi-patch-check
</span>
<span>
<i class="bi bi-patch-exclamation"></i>
bi bi-patch-exclamation
</span>
<span>
<i class="bi bi-patch-minus"></i>
bi bi-patch-minus
</span>
<span>
<i class="bi bi-patch-plus"></i>
bi bi-patch-plus
</span>
<span>
<i class="bi bi-patch-question"></i>
bi bi-patch-question
</span>
<span>
<i class="bi bi-pause"></i>
bi bi-pause
</span>
<span>
<i class="bi bi-pause-btn"></i>
bi bi-pause-btn
</span>
<span>
<i class="bi bi-pause-circle"></i>
bi bi-pause-circle
</span>
<span>
<i class="bi bi-paypal"></i>
bi bi-paypal
</span>
<span>
<i class="bi bi-pc"></i>
bi bi-pc
</span>
<span>
<i class="bi bi-pc-display"></i>
bi bi-pc-display
</span>
<span>
<i class="bi bi-pc-display-horizontal"></i>
bi bi-pc-display-horizontal
</span>
<span>
<i class="bi bi-pc-horizontal"></i>
bi bi-pc-horizontal
</span>
<span>
<i class="bi bi-pci-card"></i>
bi bi-pci-card
</span>
<span>
<i class="bi bi-pci-card-network"></i>
bi bi-pci-card-network
</span>
<span>
<i class="bi bi-pci-card-sound"></i>
bi bi-pci-card-sound
</span>
<span>
<i class="bi bi-peace"></i>
bi bi-peace
</span>
<span>
<i class="bi bi-pen"></i>
bi bi-pen
</span>
<span>
<i class="bi bi-pencil"></i>
bi bi-pencil
</span>
<span>
<i class="bi bi-pencil-square"></i>
bi bi-pencil-square
</span>
<span>
<i class="bi bi-pentagon"></i>
bi bi-pentagon
</span>
<span>
<i class="bi bi-pentagon-half"></i>
bi bi-pentagon-half
</span>
<span>
<i class="bi bi-people"></i>
bi bi-people
</span>
<span>
<i class="bi bi-person-circle"></i>
bi bi-person-circle
</span>
<span>
<i class="bi bi-percent"></i>
bi bi-percent
</span>
<span>
<i class="bi bi-perplexity"></i>
bi bi-perplexity
</span>
<span>
<i class="bi bi-person"></i>
bi bi-person
</span>
<span>
<i class="bi bi-person-add"></i>
bi bi-person-add
</span>
<span>
<i class="bi bi-person-arms-up"></i>
bi bi-person-arms-up
</span>
<span>
<i class="bi bi-person-badge"></i>
bi bi-person-badge
</span>
<span>
<i class="bi bi-person-bounding-box"></i>
bi bi-person-bounding-box
</span>
<span>
<i class="bi bi-person-check"></i>
bi bi-person-check
</span>
<span>
<i class="bi bi-person-dash"></i>
bi bi-person-dash
</span>
<span>
<i class="bi bi-person-down"></i>
bi bi-person-down
</span>
<span>
<i class="bi bi-person-exclamation"></i>
bi bi-person-exclamation
</span>
<span>
<i class="bi bi-person-gear"></i>
bi bi-person-gear
</span>
<span>
<i class="bi bi-person-heart"></i>
bi bi-person-heart
</span>
<span>
<i class="bi bi-person-hearts"></i>
bi bi-person-hearts
</span>
<span>
<i class="bi bi-person-lock"></i>
bi bi-person-lock
</span>
<span>
<i class="bi bi-person-plus"></i>
bi bi-person-plus
</span>
<span>
<i class="bi bi-person-raised-hand"></i>
bi bi-person-raised-hand
</span>
<span>
<i class="bi bi-person-rolodex"></i>
bi bi-person-rolodex
</span>
<span>
<i class="bi bi-person-slash"></i>
bi bi-person-slash
</span>
<span>
<i class="bi bi-person-square"></i>
bi bi-person-square
</span>
<span>
<i class="bi bi-person-standing"></i>
bi bi-person-standing
</span>
<span>
<i class="bi bi-person-standing-dress"></i>
bi bi-person-standing-dress
</span>
<span>
<i class="bi bi-person-up"></i>
bi bi-person-up
</span>
<span>
<i class="bi bi-person-vcard"></i>
bi bi-person-vcard
</span>
<span>
<i class="bi bi-person-video"></i>
bi bi-person-video
</span>
<span>
<i class="bi bi-person-video2"></i>
bi bi-person-video2
</span>
<span>
<i class="bi bi-person-video3"></i>
bi bi-person-video3
</span>
<span>
<i class="bi bi-person-walking"></i>
bi bi-person-walking
</span>
<span>
<i class="bi bi-person-wheelchair"></i>
bi bi-person-wheelchair
</span>
<span>
<i class="bi bi-person-workspace"></i>
bi bi-person-workspace
</span>
<span>
<i class="bi bi-person-x"></i>
bi bi-person-x
</span>
<span>
<i class="bi bi-phone"></i>
bi bi-phone
</span>
<span>
<i class="bi bi-phone-flip"></i>
bi bi-phone-flip
</span>
<span>
<i class="bi bi-phone-landscape"></i>
bi bi-phone-landscape
</span>
<span>
<i class="bi bi-phone-vibrate"></i>
bi bi-phone-vibrate
</span>
<span>
<i class="bi bi-pie-chart"></i>
bi bi-pie-chart
</span>
<span>
<i class="bi bi-piggy-bank"></i>
bi bi-piggy-bank
</span>
<span>
<i class="bi bi-pin"></i>
bi bi-pin
</span>
<span>
<i class="bi bi-pin-angle"></i>
bi bi-pin-angle
</span>
<span>
<i class="bi bi-pin-map"></i>
bi bi-pin-map
</span>
<span>
<i class="bi bi-pinterest"></i>
bi bi-pinterest
</span>
<span>
<i class="bi bi-pip"></i>
bi bi-pip
</span>
<span>
<i class="bi bi-play"></i>
bi bi-play
</span>
<span>
<i class="bi bi-play-btn"></i>
bi bi-play-btn
</span>
<span>
<i class="bi bi-play-circle"></i>
bi bi-play-circle
</span>
<span>
<i class="bi bi-playstation"></i>
bi bi-playstation
</span>
<span>
<i class="bi bi-plug"></i>
bi bi-plug
</span>
<span>
<i class="bi bi-plugin"></i>
bi bi-plugin
</span>
<span>
<i class="bi bi-plus"></i>
bi bi-plus
</span>
<span>
<i class="bi bi-plus-circle"></i>
bi bi-plus-circle
</span>
<span>
<i class="bi bi-plus-circle-dotted"></i>
bi bi-plus-circle-dotted
</span>
<span>
<i class="bi bi-plus-lg"></i>
bi bi-plus-lg
</span>
<span>
<i class="bi bi-plus-slash-minus"></i>
bi bi-plus-slash-minus
</span>
<span>
<i class="bi bi-plus-square"></i>
bi bi-plus-square
</span>
<span>
<i class="bi bi-plus-square-dotted"></i>
bi bi-plus-square-dotted
</span>
<span>
<i class="bi bi-postage"></i>
bi bi-postage
</span>
<span>
<i class="bi bi-postage-heart"></i>
bi bi-postage-heart
</span>
<span>
<i class="bi bi-postcard"></i>
bi bi-postcard
</span>
<span>
<i class="bi bi-postcard-heart"></i>
bi bi-postcard-heart
</span>
<span>
<i class="bi bi-power"></i>
bi bi-power
</span>
<span>
<i class="bi bi-prescription"></i>
bi bi-prescription
</span>
<span>
<i class="bi bi-prescription2"></i>
bi bi-prescription2
</span>
<span>
<i class="bi bi-printer"></i>
bi bi-printer
</span>
<span>
<i class="bi bi-projector"></i>
bi bi-projector
</span>
<span>
<i class="bi bi-puzzle"></i>
bi bi-puzzle
</span>
<span>
<i class="bi bi-qr-code"></i>
bi bi-qr-code
</span>
<span>
<i class="bi bi-qr-code-scan"></i>
bi bi-qr-code-scan
</span>
<span>
<i class="bi bi-question"></i>
bi bi-question
</span>
<span>
<i class="bi bi-question-circle"></i>
bi bi-question-circle
</span>
<span>
<i class="bi bi-question-diamond"></i>
bi bi-question-diamond
</span>
<span>
<i class="bi bi-question-lg"></i>
bi bi-question-lg
</span>
<span>
<i class="bi bi-question-octagon"></i>
bi bi-question-octagon
</span>
<span>
<i class="bi bi-question-square"></i>
bi bi-question-square
</span>
<span>
<i class="bi bi-quora"></i>
bi bi-quora
</span>
<span>
<i class="bi bi-quote"></i>
bi bi-quote
</span>
<span>
<i class="bi bi-r-circle"></i>
bi bi-r-circle
</span>
<span>
<i class="bi bi-r-square"></i>
bi bi-r-square
</span>
<span>
<i class="bi bi-radar"></i>
bi bi-radar
</span>
<span>
<i class="bi bi-radioactive"></i>
bi bi-radioactive
</span>
<span>
<i class="bi bi-rainbow"></i>
bi bi-rainbow
</span>
<span>
<i class="bi bi-receipt"></i>
bi bi-receipt
</span>
<span>
<i class="bi bi-receipt-cutoff"></i>
bi bi-receipt-cutoff
</span>
<span>
<i class="bi bi-reception-0"></i>
bi bi-reception-0
</span>
<span>
<i class="bi bi-reception-1"></i>
bi bi-reception-1
</span>
<span>
<i class="bi bi-reception-2"></i>
bi bi-reception-2
</span>
<span>
<i class="bi bi-reception-3"></i>
bi bi-reception-3
</span>
<span>
<i class="bi bi-reception-4"></i>
bi bi-reception-4
</span>
<span>
<i class="bi bi-record"></i>
bi bi-record
</span>
<span>
<i class="bi bi-record-btn"></i>
bi bi-record-btn
</span>
<span>
<i class="bi bi-record-circle"></i>
bi bi-record-circle
</span>
<span>
<i class="bi bi-record2"></i>
bi bi-record2
</span>
<span>
<i class="bi bi-recycle"></i>
bi bi-recycle
</span>
<span>
<i class="bi bi-reddit"></i>
bi bi-reddit
</span>
<span>
<i class="bi bi-regex"></i>
bi bi-regex
</span>
<span>
<i class="bi bi-repeat"></i>
bi bi-repeat
</span>
<span>
<i class="bi bi-repeat-1"></i>
bi bi-repeat-1
</span>
<span>
<i class="bi bi-reply"></i>
bi bi-reply
</span>
<span>
<i class="bi bi-reply-all"></i>
bi bi-reply-all
</span>
<span>
<i class="bi bi-rewind"></i>
bi bi-rewind
</span>
<span>
<i class="bi bi-rewind-btn"></i>
bi bi-rewind-btn
</span>
<span>
<i class="bi bi-rewind-circle"></i>
bi bi-rewind-circle
</span>
<span>
<i class="bi bi-robot"></i>
bi bi-robot
</span>
<span>
<i class="bi bi-rocket"></i>
bi bi-rocket
</span>
<span>
<i class="bi bi-rocket-takeoff"></i>
bi bi-rocket-takeoff
</span>
<span>
<i class="bi bi-router"></i>
bi bi-router
</span>
<span>
<i class="bi bi-rss"></i>
bi bi-rss
</span>
<span>
<i class="bi bi-rulers"></i>
bi bi-rulers
</span>
<span>
<i class="bi bi-safe"></i>
bi bi-safe
</span>
<span>
<i class="bi bi-safe2"></i>
bi bi-safe2
</span>
<span>
<i class="bi bi-save"></i>
bi bi-save
</span>
<span>
<i class="bi bi-save2"></i>
bi bi-save2
</span>
<span>
<i class="bi bi-scissors"></i>
bi bi-scissors
</span>
<span>
<i class="bi bi-scooter"></i>
bi bi-scooter
</span>
<span>
<i class="bi bi-screwdriver"></i>
bi bi-screwdriver
</span>
<span>
<i class="bi bi-sd-card"></i>
bi bi-sd-card
</span>
<span>
<i class="bi bi-search"></i>
bi bi-search
</span>
<span>
<i class="bi bi-search-heart"></i>
bi bi-search-heart
</span>
<span>
<i class="bi bi-segmented-nav"></i>
bi bi-segmented-nav
</span>
<span>
<i class="bi bi-send"></i>
bi bi-send
</span>
<span>
<i class="bi bi-send-arrow-down"></i>
bi bi-send-arrow-down
</span>
<span>
<i class="bi bi-send-arrow-up"></i>
bi bi-send-arrow-up
</span>
<span>
<i class="bi bi-send-check"></i>
bi bi-send-check
</span>
<span>
<i class="bi bi-send-dash"></i>
bi bi-send-dash
</span>
<span>
<i class="bi bi-send-exclamation"></i>
bi bi-send-exclamation
</span>
<span>
<i class="bi bi-send-plus"></i>
bi bi-send-plus
</span>
<span>
<i class="bi bi-send-slash"></i>
bi bi-send-slash
</span>
<span>
<i class="bi bi-send-x"></i>
bi bi-send-x
</span>
<span>
<i class="bi bi-server"></i>
bi bi-server
</span>
<span>
<i class="bi bi-shadows"></i>
bi bi-shadows
</span>
<span>
<i class="bi bi-share"></i>
bi bi-share
</span>
<span>
<i class="bi bi-shield"></i>
bi bi-shield
</span>
<span>
<i class="bi bi-shield-check"></i>
bi bi-shield-check
</span>
<span>
<i class="bi bi-shield-exclamation"></i>
bi bi-shield-exclamation
</span>
<span>
<i class="bi bi-shield-lock"></i>
bi bi-shield-lock
</span>
<span>
<i class="bi bi-shield-minus"></i>
bi bi-shield-minus
</span>
<span>
<i class="bi bi-shield-plus"></i>
bi bi-shield-plus
</span>
<span>
<i class="bi bi-shield-shaded"></i>
bi bi-shield-shaded
</span>
<span>
<i class="bi bi-shield-slash"></i>
bi bi-shield-slash
</span>
<span>
<i class="bi bi-shield-x"></i>
bi bi-shield-x
</span>
<span>
<i class="bi bi-shift"></i>
bi bi-shift
</span>
<span>
<i class="bi bi-shop"></i>
bi bi-shop
</span>
<span>
<i class="bi bi-shop-window"></i>
bi bi-shop-window
</span>
<span>
<i class="bi bi-shuffle"></i>
bi bi-shuffle
</span>
<span>
<i class="bi bi-sign-dead-end"></i>
bi bi-sign-dead-end
</span>
<span>
<i class="bi bi-sign-do-not-enter"></i>
bi bi-sign-do-not-enter
</span>
<span>
<i class="bi bi-sign-intersection"></i>
bi bi-sign-intersection
</span>
<span>
<i class="bi bi-sign-intersection-side"></i>
bi bi-sign-intersection-side
</span>
<span>
<i class="bi bi-sign-intersection-t"></i>
bi bi-sign-intersection-t
</span>
<span>
<i class="bi bi-sign-intersection-y"></i>
bi bi-sign-intersection-y
</span>
<span>
<i class="bi bi-sign-merge-left"></i>
bi bi-sign-merge-left
</span>
<span>
<i class="bi bi-sign-merge-right"></i>
bi bi-sign-merge-right
</span>
<span>
<i class="bi bi-sign-no-left-turn"></i>
bi bi-sign-no-left-turn
</span>
<span>
<i class="bi bi-sign-no-parking"></i>
bi bi-sign-no-parking
</span>
<span>
<i class="bi bi-sign-no-right-turn"></i>
bi bi-sign-no-right-turn
</span>
<span>
<i class="bi bi-sign-railroad"></i>
bi bi-sign-railroad
</span>
<span>
<i class="bi bi-sign-stop"></i>
bi bi-sign-stop
</span>
<span>
<i class="bi bi-sign-stop-lights"></i>
bi bi-sign-stop-lights
</span>
<span>
<i class="bi bi-sign-turn-left"></i>
bi bi-sign-turn-left
</span>
<span>
<i class="bi bi-sign-turn-right"></i>
bi bi-sign-turn-right
</span>
<span>
<i class="bi bi-sign-turn-slight-left"></i>
bi bi-sign-turn-slight-left
</span>
<span>
<i class="bi bi-sign-turn-slight-right"></i>
bi bi-sign-turn-slight-right
</span>
<span>
<i class="bi bi-sign-yield"></i>
bi bi-sign-yield
</span>
<span>
<i class="bi bi-signal"></i>
bi bi-signal
</span>
<span>
<i class="bi bi-signpost"></i>
bi bi-signpost
</span>
<span>
<i class="bi bi-signpost-2"></i>
bi bi-signpost-2
</span>
<span>
<i class="bi bi-signpost-split"></i>
bi bi-signpost-split
</span>
<span>
<i class="bi bi-sim"></i>
bi bi-sim
</span>
<span>
<i class="bi bi-sim-slash"></i>
bi bi-sim-slash
</span>
<span>
<i class="bi bi-sina-weibo"></i>
bi bi-sina-weibo
</span>
<span>
<i class="bi bi-skip-backward"></i>
bi bi-skip-backward
</span>
<span>
<i class="bi bi-skip-backward-btn"></i>
bi bi-skip-backward-btn
</span>
<span>
<i class="bi bi-skip-backward-circle"></i>
bi bi-skip-backward-circle
</span>
<span>
<i class="bi bi-skip-end"></i>
bi bi-skip-end
</span>
<span>
<i class="bi bi-skip-end-btn"></i>
bi bi-skip-end-btn
</span>
<span>
<i class="bi bi-skip-end-circle"></i>
bi bi-skip-end-circle
</span>
<span>
<i class="bi bi-skip-forward"></i>
bi bi-skip-forward
</span>
<span>
<i class="bi bi-skip-forward-btn"></i>
bi bi-skip-forward-btn
</span>
<span>
<i class="bi bi-skip-forward-circle"></i>
bi bi-skip-forward-circle
</span>
<span>
<i class="bi bi-skip-start"></i>
bi bi-skip-start
</span>
<span>
<i class="bi bi-skip-start-btn"></i>
bi bi-skip-start-btn
</span>
<span>
<i class="bi bi-skip-start-circle"></i>
bi bi-skip-start-circle
</span>
<span>
<i class="bi bi-skype"></i>
bi bi-skype
</span>
<span>
<i class="bi bi-slack"></i>
bi bi-slack
</span>
<span>
<i class="bi bi-slash"></i>
bi bi-slash
</span>
<span>
<i class="bi bi-slash-lg"></i>
bi bi-slash-lg
</span>
<span>
<i class="bi bi-slash-square"></i>
bi bi-slash-square
</span>
<span>
<i class="bi bi-sliders"></i>
bi bi-sliders
</span>
<span>
<i class="bi bi-sliders2"></i>
bi bi-sliders2
</span>
<span>
<i class="bi bi-sliders2-vertical"></i>
bi bi-sliders2-vertical
</span>
<span>
<i class="bi bi-smartwatch"></i>
bi bi-smartwatch
</span>
<span>
<i class="bi bi-snapchat"></i>
bi bi-snapchat
</span>
<span>
<i class="bi bi-snow"></i>
bi bi-snow
</span>
<span>
<i class="bi bi-snow2"></i>
bi bi-snow2
</span>
<span>
<i class="bi bi-snow3"></i>
bi bi-snow3
</span>
<span>
<i class="bi bi-sort-alpha-down"></i>
bi bi-sort-alpha-down
</span>
<span>
<i class="bi bi-sort-alpha-down-alt"></i>
bi bi-sort-alpha-down-alt
</span>
<span>
<i class="bi bi-sort-alpha-up"></i>
bi bi-sort-alpha-up
</span>
<span>
<i class="bi bi-sort-alpha-up-alt"></i>
bi bi-sort-alpha-up-alt
</span>
<span>
<i class="bi bi-sort-down"></i>
bi bi-sort-down
</span>
<span>
<i class="bi bi-sort-down-alt"></i>
bi bi-sort-down-alt
</span>
<span>
<i class="bi bi-sort-numeric-down"></i>
bi bi-sort-numeric-down
</span>
<span>
<i class="bi bi-sort-numeric-down-alt"></i>
bi bi-sort-numeric-down-alt
</span>
<span>
<i class="bi bi-sort-numeric-up"></i>
bi bi-sort-numeric-up
</span>
<span>
<i class="bi bi-sort-numeric-up-alt"></i>
bi bi-sort-numeric-up-alt
</span>
<span>
<i class="bi bi-sort-up"></i>
bi bi-sort-up
</span>
<span>
<i class="bi bi-sort-up-alt"></i>
bi bi-sort-up-alt
</span>
<span>
<i class="bi bi-soundwave"></i>
bi bi-soundwave
</span>
<span>
<i class="bi bi-sourceforge"></i>
bi bi-sourceforge
</span>
<span>
<i class="bi bi-speaker"></i>
bi bi-speaker
</span>
<span>
<i class="bi bi-speedometer"></i>
bi bi-speedometer
</span>
<span>
<i class="bi bi-speedometer2"></i>
bi bi-speedometer2
</span>
<span>
<i class="bi bi-spellcheck"></i>
bi bi-spellcheck
</span>
<span>
<i class="bi bi-spotify"></i>
bi bi-spotify
</span>
<span>
<i class="bi bi-square"></i>
bi bi-square
</span>
<span>
<i class="bi bi-square-half"></i>
bi bi-square-half
</span>
<span>
<i class="bi bi-stack"></i>
bi bi-stack
</span>
<span>
<i class="bi bi-stack-overflow"></i>
bi bi-stack-overflow
</span>
<span>
<i class="bi bi-star"></i>
bi bi-star
</span>
<span>
<i class="bi bi-star-half"></i>
bi bi-star-half
</span>
<span>
<i class="bi bi-stars"></i>
bi bi-stars
</span>
<span>
<i class="bi bi-steam"></i>
bi bi-steam
</span>
<span>
<i class="bi bi-stickies"></i>
bi bi-stickies
</span>
<span>
<i class="bi bi-sticky"></i>
bi bi-sticky
</span>
<span>
<i class="bi bi-stop"></i>
bi bi-stop
</span>
<span>
<i class="bi bi-stop-btn"></i>
bi bi-stop-btn
</span>
<span>
<i class="bi bi-stop-circle"></i>
bi bi-stop-circle
</span>
<span>
<i class="bi bi-stoplights"></i>
bi bi-stoplights
</span>
<span>
<i class="bi bi-stopwatch"></i>
bi bi-stopwatch
</span>
<span>
<i class="bi bi-strava"></i>
bi bi-strava
</span>
<span>
<i class="bi bi-stripe"></i>
bi bi-stripe
</span>
<span>
<i class="bi bi-subscript"></i>
bi bi-subscript
</span>
<span>
<i class="bi bi-substack"></i>
bi bi-substack
</span>
<span>
<i class="bi bi-subtract"></i>
bi bi-subtract
</span>
<span>
<i class="bi bi-suit-club"></i>
bi bi-suit-club
</span>
<span>
<i class="bi bi-suit-diamond"></i>
bi bi-suit-diamond
</span>
<span>
<i class="bi bi-suit-heart"></i>
bi bi-suit-heart
</span>
<span>
<i class="bi bi-suit-spade"></i>
bi bi-suit-spade
</span>
<span>
<i class="bi bi-suitcase"></i>
bi bi-suitcase
</span>
<span>
<i class="bi bi-suitcase-lg"></i>
bi bi-suitcase-lg
</span>
<span>
<i class="bi bi-suitcase2"></i>
bi bi-suitcase2
</span>
<span>
<i class="bi bi-sun"></i>
bi bi-sun
</span>
<span>
<i class="bi bi-sunglasses"></i>
bi bi-sunglasses
</span>
<span>
<i class="bi bi-sunrise"></i>
bi bi-sunrise
</span>
<span>
<i class="bi bi-sunset"></i>
bi bi-sunset
</span>
<span>
<i class="bi bi-superscript"></i>
bi bi-superscript
</span>
<span>
<i class="bi bi-symmetry-horizontal"></i>
bi bi-symmetry-horizontal
</span>
<span>
<i class="bi bi-symmetry-vertical"></i>
bi bi-symmetry-vertical
</span>
<span>
<i class="bi bi-table"></i>
bi bi-table
</span>
<span>
<i class="bi bi-tablet"></i>
bi bi-tablet
</span>
<span>
<i class="bi bi-tablet-landscape"></i>
bi bi-tablet-landscape
</span>
<span>
<i class="bi bi-tag"></i>
bi bi-tag
</span>
<span>
<i class="bi bi-tags"></i>
bi bi-tags
</span>
<span>
<i class="bi bi-taxi-front"></i>
bi bi-taxi-front
</span>
<span>
<i class="bi bi-telegram"></i>
bi bi-telegram
</span>
<span>
<i class="bi bi-telephone"></i>
bi bi-telephone
</span>
<span>
<i class="bi bi-telephone-forward"></i>
bi bi-telephone-forward
</span>
<span>
<i class="bi bi-telephone-inbound"></i>
bi bi-telephone-inbound
</span>
<span>
<i class="bi bi-telephone-minus"></i>
bi bi-telephone-minus
</span>
<span>
<i class="bi bi-telephone-outbound"></i>
bi bi-telephone-outbound
</span>
<span>
<i class="bi bi-telephone-plus"></i>
bi bi-telephone-plus
</span>
<span>
<i class="bi bi-telephone-x"></i>
bi bi-telephone-x
</span>
<span>
<i class="bi bi-tencent-qq"></i>
bi bi-tencent-qq
</span>
<span>
<i class="bi bi-terminal"></i>
bi bi-terminal
</span>
<span>
<i class="bi bi-terminal-dash"></i>
bi bi-terminal-dash
</span>
<span>
<i class="bi bi-terminal-plus"></i>
bi bi-terminal-plus
</span>
<span>
<i class="bi bi-terminal-split"></i>
bi bi-terminal-split
</span>
<span>
<i class="bi bi-terminal-x"></i>
bi bi-terminal-x
</span>
<span>
<i class="bi bi-text-center"></i>
bi bi-text-center
</span>
<span>
<i class="bi bi-text-indent-left"></i>
bi bi-text-indent-left
</span>
<span>
<i class="bi bi-text-indent-right"></i>
bi bi-text-indent-right
</span>
<span>
<i class="bi bi-text-left"></i>
bi bi-text-left
</span>
<span>
<i class="bi bi-text-paragraph"></i>
bi bi-text-paragraph
</span>
<span>
<i class="bi bi-text-right"></i>
bi bi-text-right
</span>
<span>
<i class="bi bi-text-wrap"></i>
bi bi-text-wrap
</span>
<span>
<i class="bi bi-textarea"></i>
bi bi-textarea
</span>
<span>
<i class="bi bi-textarea-resize"></i>
bi bi-textarea-resize
</span>
<span>
<i class="bi bi-textarea-t"></i>
bi bi-textarea-t
</span>
<span>
<i class="bi bi-thermometer"></i>
bi bi-thermometer
</span>
<span>
<i class="bi bi-thermometer-half"></i>
bi bi-thermometer-half
</span>
<span>
<i class="bi bi-thermometer-high"></i>
bi bi-thermometer-high
</span>
<span>
<i class="bi bi-thermometer-low"></i>
bi bi-thermometer-low
</span>
<span>
<i class="bi bi-thermometer-snow"></i>
bi bi-thermometer-snow
</span>
<span>
<i class="bi bi-thermometer-sun"></i>
bi bi-thermometer-sun
</span>
<span>
<i class="bi bi-threads"></i>
bi bi-threads
</span>
<span>
<i class="bi bi-three-dots"></i>
bi bi-three-dots
</span>
<span>
<i class="bi bi-three-dots-vertical"></i>
bi bi-three-dots-vertical
</span>
<span>
<i class="bi bi-thunderbolt"></i>
bi bi-thunderbolt
</span>
<span>
<i class="bi bi-ticket"></i>
bi bi-ticket
</span>
<span>
<i class="bi bi-ticket-detailed"></i>
bi bi-ticket-detailed
</span>
<span>
<i class="bi bi-ticket-perforated"></i>
bi bi-ticket-perforated
</span>
<span>
<i class="bi bi-tiktok"></i>
bi bi-tiktok
</span>
<span>
<i class="bi bi-toggle-off"></i>
bi bi-toggle-off
</span>
<span>
<i class="bi bi-toggle-on"></i>
bi bi-toggle-on
</span>
<span>
<i class="bi bi-toggle2-off"></i>
bi bi-toggle2-off
</span>
<span>
<i class="bi bi-toggle2-on"></i>
bi bi-toggle2-on
</span>
<span>
<i class="bi bi-toggles"></i>
bi bi-toggles
</span>
<span>
<i class="bi bi-toggles2"></i>
bi bi-toggles2
</span>
<span>
<i class="bi bi-tools"></i>
bi bi-tools
</span>
<span>
<i class="bi bi-tornado"></i>
bi bi-tornado
</span>
<span>
<i class="bi bi-train-freight-front"></i>
bi bi-train-freight-front
</span>
<span>
<i class="bi bi-train-front"></i>
bi bi-train-front
</span>
<span>
<i class="bi bi-train-lightrail-front"></i>
bi bi-train-lightrail-front
</span>
<span>
<i class="bi bi-translate"></i>
bi bi-translate
</span>
<span>
<i class="bi bi-transparency"></i>
bi bi-transparency
</span>
<span>
<i class="bi bi-trash"></i>
bi bi-trash
</span>
<span>
<i class="bi bi-trash2"></i>
bi bi-trash2
</span>
<span>
<i class="bi bi-trash3"></i>
bi bi-trash3
</span>
<span>
<i class="bi bi-tree"></i>
bi bi-tree
</span>
<span>
<i class="bi bi-trello"></i>
bi bi-trello
</span>
<span>
<i class="bi bi-triangle"></i>
bi bi-triangle
</span>
<span>
<i class="bi bi-triangle-half"></i>
bi bi-triangle-half
</span>
<span>
<i class="bi bi-trophy"></i>
bi bi-trophy
</span>
<span>
<i class="bi bi-tropical-storm"></i>
bi bi-tropical-storm
</span>
<span>
<i class="bi bi-truck"></i>
bi bi-truck
</span>
<span>
<i class="bi bi-truck-flatbed"></i>
bi bi-truck-flatbed
</span>
<span>
<i class="bi bi-truck-front"></i>
bi bi-truck-front
</span>
<span>
<i class="bi bi-tsunami"></i>
bi bi-tsunami
</span>
<span>
<i class="bi bi-tux"></i>
bi bi-tux
</span>
<span>
<i class="bi bi-tv"></i>
bi bi-tv
</span>
<span>
<i class="bi bi-twitch"></i>
bi bi-twitch
</span>
<span>
<i class="bi bi-twitter"></i>
bi bi-twitter
</span>
<span>
<i class="bi bi-twitter-x"></i>
bi bi-twitter-x
</span>
<span>
<i class="bi bi-type"></i>
bi bi-type
</span>
<span>
<i class="bi bi-type-bold"></i>
bi bi-type-bold
</span>
<span>
<i class="bi bi-type-h1"></i>
bi bi-type-h1
</span>
<span>
<i class="bi bi-type-h2"></i>
bi bi-type-h2
</span>
<span>
<i class="bi bi-type-h3"></i>
bi bi-type-h3
</span>
<span>
<i class="bi bi-type-h4"></i>
bi bi-type-h4
</span>
<span>
<i class="bi bi-type-h5"></i>
bi bi-type-h5
</span>
<span>
<i class="bi bi-type-h6"></i>
bi bi-type-h6
</span>
<span>
<i class="bi bi-type-italic"></i>
bi bi-type-italic
</span>
<span>
<i class="bi bi-type-strikethrough"></i>
bi bi-type-strikethrough
</span>
<span>
<i class="bi bi-type-underline"></i>
bi bi-type-underline
</span>
<span>
<i class="bi bi-typescript"></i>
bi bi-typescript
</span>
<span>
<i class="bi bi-ubuntu"></i>
bi bi-ubuntu
</span>
<span>
<i class="bi bi-ui-checks"></i>
bi bi-ui-checks
</span>
<span>
<i class="bi bi-ui-checks-grid"></i>
bi bi-ui-checks-grid
</span>
<span>
<i class="bi bi-ui-radios"></i>
bi bi-ui-radios
</span>
<span>
<i class="bi bi-ui-radios-grid"></i>
bi bi-ui-radios-grid
</span>
<span>
<i class="bi bi-umbrella"></i>
bi bi-umbrella
</span>
<span>
<i class="bi bi-unindent"></i>
bi bi-unindent
</span>
<span>
<i class="bi bi-union"></i>
bi bi-union
</span>
<span>
<i class="bi bi-unity"></i>
bi bi-unity
</span>
<span>
<i class="bi bi-universal-access"></i>
bi bi-universal-access
</span>
<span>
<i class="bi bi-universal-access-circle"></i>
bi bi-universal-access-circle
</span>
<span>
<i class="bi bi-unlock"></i>
bi bi-unlock
</span>
<span>
<i class="bi bi-unlock2"></i>
bi bi-unlock2
</span>
<span>
<i class="bi bi-upc"></i>
bi bi-upc
</span>
<span>
<i class="bi bi-upc-scan"></i>
bi bi-upc-scan
</span>
<span>
<i class="bi bi-upload"></i>
bi bi-upload
</span>
<span>
<i class="bi bi-usb"></i>
bi bi-usb
</span>
<span>
<i class="bi bi-usb-c"></i>
bi bi-usb-c
</span>
<span>
<i class="bi bi-usb-drive"></i>
bi bi-usb-drive
</span>
<span>
<i class="bi bi-usb-micro"></i>
bi bi-usb-micro
</span>
<span>
<i class="bi bi-usb-mini"></i>
bi bi-usb-mini
</span>
<span>
<i class="bi bi-usb-plug"></i>
bi bi-usb-plug
</span>
<span>
<i class="bi bi-usb-symbol"></i>
bi bi-usb-symbol
</span>
<span>
<i class="bi bi-valentine"></i>
bi bi-valentine
</span>
<span>
<i class="bi bi-valentine2"></i>
bi bi-valentine2
</span>
<span>
<i class="bi bi-vector-pen"></i>
bi bi-vector-pen
</span>
<span>
<i class="bi bi-view-list"></i>
bi bi-view-list
</span>
<span>
<i class="bi bi-view-stacked"></i>
bi bi-view-stacked
</span>
<span>
<i class="bi bi-vignette"></i>
bi bi-vignette
</span>
<span>
<i class="bi bi-vimeo"></i>
bi bi-vimeo
</span>
<span>
<i class="bi bi-vinyl"></i>
bi bi-vinyl
</span>
<span>
<i class="bi bi-virus"></i>
bi bi-virus
</span>
<span>
<i class="bi bi-virus2"></i>
bi bi-virus2
</span>
<span>
<i class="bi bi-voicemail"></i>
bi bi-voicemail
</span>
<span>
<i class="bi bi-volume-down"></i>
bi bi-volume-down
</span>
<span>
<i class="bi bi-volume-mute"></i>
bi bi-volume-mute
</span>
<span>
<i class="bi bi-volume-off"></i>
bi bi-volume-off
</span>
<span>
<i class="bi bi-volume-up"></i>
bi bi-volume-up
</span>
<span>
<i class="bi bi-vr"></i>
bi bi-vr
</span>
<span>
<i class="bi bi-wallet"></i>
bi bi-wallet
</span>
<span>
<i class="bi bi-wallet2"></i>
bi bi-wallet2
</span>
<span>
<i class="bi bi-watch"></i>
bi bi-watch
</span>
<span>
<i class="bi bi-water"></i>
bi bi-water
</span>
<span>
<i class="bi bi-webcam"></i>
bi bi-webcam
</span>
<span>
<i class="bi bi-wechat"></i>
bi bi-wechat
</span>
<span>
<i class="bi bi-whatsapp"></i>
bi bi-whatsapp
</span>
<span>
<i class="bi bi-wifi"></i>
bi bi-wifi
</span>
<span>
<i class="bi bi-wifi-1"></i>
bi bi-wifi-1
</span>
<span>
<i class="bi bi-wifi-2"></i>
bi bi-wifi-2
</span>
<span>
<i class="bi bi-wifi-off"></i>
bi bi-wifi-off
</span>
<span>
<i class="bi bi-wikipedia"></i>
bi bi-wikipedia
</span>
<span>
<i class="bi bi-wind"></i>
bi bi-wind
</span>
<span>
<i class="bi bi-window"></i>
bi bi-window
</span>
<span>
<i class="bi bi-window-dash"></i>
bi bi-window-dash
</span>
<span>
<i class="bi bi-window-desktop"></i>
bi bi-window-desktop
</span>
<span>
<i class="bi bi-window-dock"></i>
bi bi-window-dock
</span>
<span>
<i class="bi bi-window-fullscreen"></i>
bi bi-window-fullscreen
</span>
<span>
<i class="bi bi-window-plus"></i>
bi bi-window-plus
</span>
<span>
<i class="bi bi-window-sidebar"></i>
bi bi-window-sidebar
</span>
<span>
<i class="bi bi-window-split"></i>
bi bi-window-split
</span>
<span>
<i class="bi bi-window-stack"></i>
bi bi-window-stack
</span>
<span>
<i class="bi bi-window-x"></i>
bi bi-window-x
</span>
<span>
<i class="bi bi-windows"></i>
bi bi-windows
</span>
<span>
<i class="bi bi-wordpress"></i>
bi bi-wordpress
</span>
<span>
<i class="bi bi-wrench"></i>
bi bi-wrench
</span>
<span>
<i class="bi bi-wrench-adjustable"></i>
bi bi-wrench-adjustable
</span>
<span>
<i class="bi bi-wrench-adjustable-circle"></i>
bi bi-wrench-adjustable-circle
</span>
<span>
<i class="bi bi-x"></i>
bi bi-x
</span>
<span>
<i class="bi bi-x-circle"></i>
bi bi-x-circle
</span>
<span>
<i class="bi bi-x-diamond"></i>
bi bi-x-diamond
</span>
<span>
<i class="bi bi-x-lg"></i>
bi bi-x-lg
</span>
<span>
<i class="bi bi-x-octagon"></i>
bi bi-x-octagon
</span>
<span>
<i class="bi bi-x-square"></i>
bi bi-x-square
</span>
<span>
<i class="bi bi-xbox"></i>
bi bi-xbox
</span>
<span>
<i class="bi bi-yelp"></i>
bi bi-yelp
</span>
<span>
<i class="bi bi-yin-yang"></i>
bi bi-yin-yang
</span>
<span>
<i class="bi bi-youtube"></i>
bi bi-youtube
</span>
<span>
<i class="bi bi-zoom-in"></i>
bi bi-zoom-in
</span>
<span>
<i class="bi bi-zoom-out"></i>
bi bi-zoom-out
</span>

    
  </div>
</template>