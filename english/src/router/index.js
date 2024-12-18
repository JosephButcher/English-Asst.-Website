import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import RootsComponent from '../components/RootsComponent.vue';
import VocabularyComponent from '../components/VocabularyComponent.vue';
import FiguresOfSpeechComponent from '../components/FiguresOfSpeechComponent.vue';
import ConfusingWordsComponent from '../components/ConfusingWordsComponent.vue';
import AccountComponent from '../components/AccountComponent.vue';
import VocabPracticeComponent from '../components/VocabPracticeComponent.vue';

const routes = [
    { path: '/', component: HomeComponent },
    { path: '/RootsComponent', component: RootsComponent },
    { path: '/VocabularyComponent', component: VocabularyComponent },
    { path: '/FiguresOfSpeechComponent', component: FiguresOfSpeechComponent },
    { path: '/ConfusingWordsComponent', component: ConfusingWordsComponent },
    { path: '/AccountComponent', component: AccountComponent },
    { path: '/VocabPracticeComponent', component: VocabPracticeComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;