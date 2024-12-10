<script setup>
import { ref } from "vue";

const isVisible = ref(true);
const closeWindow = () => {
  isVisible.value = false;
};

const data = ref ([{
  word: "Happy",
  pronunciation: "hæpi",
  definition: "Feeling or showing pleasure or contentment.",
  example: "She was happy with her results.",
  synonyms: ["Joyful", "content", "pleased"]
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
        <p class="pronunciation"><strong>Pronunciation:&nbsp;</strong>{{ item.pronunciation }}</p>
        <p class="definition"><strong>Definition:&nbsp;</strong>{{ item.definition }}</p>
        <p class="example"><strong>Example:&nbsp;</strong>{{ item.example }}</p>
        <p class="synonyms"><strong>Synonyms:&nbsp;</strong>{{ item.synonyms.join(', ') }}</p>
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
  width: 50vw;
  height: 95vh;
  background: whitesmoke;
  border-radius: 15px;
  padding: 15px;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
  width: 8%;
  font-size: 1vw;
  color: #4A4A4A;
}
.window-content {
  padding: 15px;
  border-bottom: 1px solid #ddd;
}
.word {
  font-size: 1.125vw;
}
.pronunciation {
  font-size: 1vw;
  font-weight: lighter;
}
.definition {
  font-size: 1vw;
}
.example {
  font-size: 1vw;
  font-style: italic;
}
.synonyms {
  font-size: 1vw;
}
h2 {
  color: #4A4A4A;
}
</style>