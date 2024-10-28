import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Roots from '../components/Roots.vue';
import Vocabulary from '../components/Vocabulary.vue';
import FiguresOfSpeech from '../components/FiguresOfSpeech.vue';
import ConfusingWords from '../components/ConfusingWords.vue';
import Account from '../components/Account.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/Roots', component: Roots },
    { path: '/Vocabulary', component: Vocabulary },
    { path: '/FiguresOfSpeech', component: FiguresOfSpeech },
    { path: '/ConfusingWords', component: ConfusingWords },
    { path: '/Account', component: Account },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;