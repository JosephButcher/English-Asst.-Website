<script setup>
import NavBar from "./NavBarComponent.vue";
import { reactive, ref} from "vue";

const formData = reactive({
  name: '',
  email: '',
  password: '',
});

const isSubmitted = ref(false);

function handleSubmit() {
  isSubmitted.value = true;
  console.log("Form submitted with: ", formData);
}
</script>

<template>
  <main>
  <NavBar />
    <h1>Account</h1>
    <div>
      <form @submit.prevent="handleSubmit" class="container">
        <fieldset>
          <input type="text" id="name" v-model="formData.name" placeholder="Name" required><br>
          <input type="email" id="email" v-model="formData.email" placeholder="Email" required><br>
          <input type="password" id="password" v-model="formData.password" placeholder="Password" required><br>
          <button type="submit">
            {{ isSubmitted ? "Change Information" : "Submit Information" }}
          </button>
        </fieldset>
      </form>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: #FFFFFF;
}
h1 {
  align-self: center;
  text-align: center;
  position: relative;
  color: #4A4A4A;
  width: 18%;
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
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 60%;
  width: 100%;
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 80%;
}
fieldset {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  width: 100%;
  background-color: #F8F8FF;
  border: none;
}
input, button {
  align-self: center;
  position: relative;
  width: 25%;
  border: none;
  border-bottom: 2px solid #D3D3D3;
  margin-bottom: 6px;
  padding: 6px;
  border-radius: 30px;
  font-size: 1.2em;
}
button {
  width: 25%;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  background-color: #76c4fa;
  color: #4A4A4A;
}
button:hover {
  background-color:  #6aa7d1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>