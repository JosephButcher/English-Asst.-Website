<script setup>
import NavBar from "./NavBarComponent.vue";
</script>

<template>
  <main>
  <NavBar />
    <h1>Account</h1>
    <div>
      <form method="post" class="container">
        <fieldset>
          <input type="text" name="name" placeholder="Name" required><br>
          <input type="email" name="email" placeholder="Email" required><br>
          <input type="password" name="password" placeholder="Password" required><br>
          <input type="submit" value="Change Information">
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
input {
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
input[type="submit"] {
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  background-color: #76c4fa;
  color: #4A4A4A;
}
input[type="submit"]:hover {
  background-color:  #6aa7d1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>