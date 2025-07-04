import { createApp, ref } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';

// Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// Global styles
// import './style.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// #todo figure out best way to add constants... see how i18n done
app.config.globalProperties.$entitiesIcon = ref('bi bi-building');
app.provide('entitiesIcon', 'bi bi-building')
app.config.globalProperties.$positionsIcon = ref('bi bi-briefcase');


app.mount('#app');
