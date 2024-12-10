<script setup>
import { ref } from "vue";

const isVisible = ref(true);
const closeWindow = () => {
  isVisible.value = false;
  window.history.back();
};

const data = ref ([{
  word: "Inquisitive",
  partOfSpeech: "Adjective",
  definition: "Curious or eager to learn; inclined to ask questions.",
  example: "The inquisitive student asked numerous questions during the lecture to fully understand the topic.",
  synonyms: ["Nosy", "analytical"]
}])
</script>

<template>
  <div class="overlay" v-if="isVisible">
    <div class="window">
      <div class="window-header">
        <h2>Vocabulary Practice</h2>
        <button class="exit-button" @click="closeWindow">Exit</button>
      </div>
      <div v-for="(item, index) in data" :key="index" class="window-content">
        <h3 class="word">{{ item.word }}</h3>
        <p class="partOfSpeech"><strong>Part of Speech:&nbsp;</strong>{{ item.partOfSpeech }}</p>
        <p class="definition"><strong>Definition:&nbsp;</strong>{{ item.definition }}</p>
        <p class="example"><strong>Example:&nbsp;</strong>{{ item.example }}</p>
        <p class="synonyms"><strong>Synonyms:&nbsp;</strong>{{ item.synonyms.join(', ') }}</p>
      </div>
      <div class="continue-button-container">
        <button class="continue-button" @click="Continue">Continue</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.window{
  width: 65vw;
  height: 85vh;
  background: whitesmoke;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
}
.window-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 2px solid #4A4A4A;
}
.exit-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1vw;
  color: #4A4A4A;
}
.window-content {
  padding: 15px 0;
}
.word {
  font-size: 1.5rem;
  color: #007BFF;
}
.partOfSpeech, .definition, .example, .synonyms {
  font-size: 1.125rem;
  margin: 5px 0;
  color: #4A4A4A;
}
.partOfSpeech strong, .definition strong, .example strong, .synonyms strong {
  color: #000080;
}
h2 {
  color: #4A4A4A;
}
.continue-button-container {
  border-top: 2px solid #4A4A4A;
  padding-top: 10px;
}
.continue-button {
  width: 100%;
  padding: 10px;
  margin-top: auto;
  background-color: #76c4fa;
  color: whitesmoke;
  font-size: 1.25rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.continue-button:hover {
  background-color: #6aa7d1;
}
</style>