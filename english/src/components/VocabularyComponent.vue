<script setup>
import NavBar from './NavBarComponent.vue';
import vocabExample from '../assets/images/vocabExample.png';
</script>

<template>
  <NavBar />

  <div class="container">

    <h1>Vocabulary</h1>
    <h3>Welcome to our vocabulary page!</h3>
    <br>
    <!-- generated with ChatGPT -->
    <p>At our core, we are dedicated to empowering learners with a robust and expansive vocabulary, cultivating their ability to communicate with eloquence and precision in every aspect of their daily lives. Our mission is to guide students toward becoming more articulate speakers and confident writers, equipped to navigate academic, professional, and personal interactions with ease.

      We offer a comprehensive collection of hundreds of carefully curated words, tailored to suit learners at every level—from inquisitive sixth graders eager to expand their linguistic horizons to seasoned seniors refining their language skills. Whether you're just beginning your journey into the world of advanced vocabulary or striving to master the subtleties of expression, you'll find that our program has something valuable for everyone.

      Through engaging lessons and dynamic exercises, we aspire to inspire a lifelong appreciation for the power of words, ensuring that our learners not only build their vocabulary but also gain the tools they need to express themselves with clarity, confidence, and impact.</p>

    <div class="example-container">
      <main class="example-window"><img :src="vocabExample" alt="Vocabulary practice example"></main>
      <div class="example-explanation">
        <p>This image is an example of what practicing vocabulary is like. Learners are presented with a new word accompanied by its part of speech, definition, an example use of the word, and a synonym or two. Learners are expected to read through all of the information and hit the continue button, where they will be taken to a spelling question, and after that the new word will be added to a mix of all the words they've learned. This cycle will continue as students learn new words and are quizzed on each word they've passed the spelling question for.</p>
        <p>If a learner fails the spelling question, they will simply be redirected to the previous screen.</p>
      </div>
    </div>
    <button @click="$router.push('/VocabPracticeComponent')" class="practice-button">Start Practicing</button>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding-top: calc(5vh + 2rem);
}
.example-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  width: 80%;
  margin-top: 2rem;
}
.example-window {
  display: flex;
  position: relative;
  height: 69vh;
  width: 85vw;
  border: 6px double #4A4A4A;
  border-radius: 10px;
  margin: 1.3rem 1rem auto 2rem;
}
.example-window img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
h1 {
  text-align: center;
  position: relative;
  color: #4A4A4A;
  width: 22%;
  margin-bottom: 2%;
  font-size: 4vw;
}
h1::after{
  content: "";
  display: block;
  position: absolute;
  width: 100%;
  height: 8px;
  background-color: #4A4A4A;
  margin-top: 5px;
  margin-bottom: .3%;
}
h3 {
  text-align: center;
  font-size: 1.5vw;
  font-weight: bold;
  color: #1A1A1A;
}
.example-explanation{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 50%;
  height: 100%;
}
.example-explanation p, p {
  text-align: center;
  color: #333;
  width: 80%;
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 1%;
  font-size: 1.125vw;
  line-height: 1.6;
}
.practice-button {
  color: whitesmoke;
  background-color: #76c4fa;
  cursor: pointer;
  border: 2px outset whitesmoke;
  border-radius: 15px;
  height: 30%;
  width: 80%;
  padding: 1%;
  margin: 1.5rem 0 0 0;
  font-size: 1.5vw;
}
.practice-button:hover {
  background-color: #6aa7d1;
  border: 2px inset whitesmoke;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>