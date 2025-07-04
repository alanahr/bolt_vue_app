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

app.config.globalProperties.$entitiesIcon = ref('bi bi-building');
app.config.globalProperties.$positionsIcon = ref('bi bi-briefcase');


app.mount('#app');
