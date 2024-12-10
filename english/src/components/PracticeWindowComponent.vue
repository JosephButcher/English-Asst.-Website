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
        <p class="partOfSpeech">{{ item.partOfSpeech }}</p>
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
  width: 8%;
  cursor: pointer;
  font-size: 2vw;
  color: #4A4A4A;
}
.exit-button:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
.window-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 0 20px 0;
  height: 80%;
}
.word {
  display: flex;
  justify-content: left;
  align-items: flex-start;
  font-size: 3.5rem;
  color: #007BFF;
  margin: 1vh auto 1vh 1vh;
}
.partOfSpeech {
  display: flex;
  justify-content: left;
  align-items: flex-start;
}
.partOfSpeech, .definition, .example, .synonyms {
  font-size: 2.5vh;
  margin: 3vh auto 3vh 1vh;
  color: #4A4A4A;
}
.definition strong, .example strong, .synonyms strong {
  color: #000080;
  font-style: italic;
}
h2 {
  font-size: 4vh;
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