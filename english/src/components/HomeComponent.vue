<script setup>
import NavBar from "./NavBarComponent.vue";
</script>

<template>
  <NavBar />
  <main class="container">
    <div class="introduction">
      <h1>Welcome to JoJaMi</h1>
      <h3>Pronounced joe&bull;jah&bull;mee</h3>
      <br>
        <p>Welcome to our English assistant website! This website is designed to assist middle school and lower high school students expand their knowledge of topics including Latin and Greek roots, general vocabulary, figures of speech, and commonly confused words. Each of these topics will be available for learners to engage in at any time, but the preferred progression is for learners to move from the roots, to vocabulary, to figures speech, and to end their learning journey with commonly confused words. But again, learners may learn whatever they choose at any time!</p>
      <br>
    </div>
    <div class="roots">
      <h2>Latin and Greek Roots</h2>
        <p>Latin and Greek roots are a new way to start learning vocabulary easier. Being able to recognize a root they've already learned allows them to more easily deduce, and remember, what a new word means. Because this has found to be helpful as it's been practiced, we'd like to give all learners the chance to learn a skill they never had the chance to, or for learners to continue practicing!</p>
    </div>
    <div class="vocabulary">
      <h2>Vocabulary</h2>
        <p>Vocabulary is an essential component in any person's life, and building it from a young age is invaluable. A robust vocabulary may enrich learning across various subjects, such as history, math, and science, enabling learners to engage with complex language. The vocabulary provided here is aimed at learners from ages 12 to 16.</p>
    </div>
    <div class="figuresOfSpeech">
      <h2>Figures of Speech</h2>
        <p>Figures of speech are words or phrases that deviate from literal definitions and meanings to create an effect. Some common examples of figures of speech are metaphors, similes, hyperboles, alliteration, and there's plenty more. Although these aren't vital for someone's language skills, being able to recognize and use them efficiently may vastly expand their language proficiency.</p>
    </div>
    <div class="commonlyConfusedWords">
      <h2>Commonly Confused Words</h2>
        <p>Commonly confused words is a topic we are excited to introduce based loosely on what people tend to confuse in their daily speech. These confusions come from both verbal and written communication. To make what this topic means a little clearer, here are a few examples. Further vs. farther, weather vs. whether, and they're vs. their vs. there.</p>
    </div>
  </main>
</template>


<style scoped>
* {
  margin: 0;
  padding: 0;
}
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding-top: calc(4vh);
}
main div {
  text-align: center;
  height: auto;
  width: 100%;
}
.introduction {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin: 4% 0;
}
h1 {
  text-align: center;
  position: relative;
  color: #4A4A4A;
  width: 50%;
  margin-bottom: 2%;
  font-size: 5vw;
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
  padding: 0 0 .5%;
}
p {
  font-size: 1.125vw;
  color: #4A4A4A;
}
.introduction p {
  width: 40%;
}
.roots, .vocabulary, .figuresOfSpeech, .commonlyConfusedWords {
  display: flex;
  text-align: center;
  align-items: center;
  flex-wrap: wrap;
}
.roots, .figuresOfSpeech {
  flex-direction: row;
  justify-content: space-around;
  background: #bbe3f8;
}
.vocabulary, .commonlyConfusedWords {
  flex-direction: row-reverse;
  justify-content: space-around;
  background: #c7efd2;
}
.figuresOfSpeech {
  background: #d1d1e1;
}
.commonlyConfusedWords {
  background: #c9e4f3;
}
.roots p, .figuresOfSpeech p, .vocabulary p, .commonlyConfusedWords p{
  padding: 2%;
  width: 25%;
}
</style>