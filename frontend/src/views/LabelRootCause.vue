<template>
  <div class="main">
    <div class="left" style="border: 1px rgb(147, 145, 145) solid;">
      <TimePeriod></TimePeriod>
    </div>

    <div class="right">
      <div style="display: flex;margin: 10px 0;">
        <div style="width: 2px;background-color: rgb(88,162,252);"></div>
        <div style="color: black; font-size: 16px;">&nbsp;&nbsp;&nbsp;Topological Relationship Diagram</div>
      </div>

      <div style="display: flex;margin: 10px 0;">
        <svg width="128" height="20">
          <circle cx="120" cy="10" r="8" fill="#61a8e0" />
        </svg>
        <div style="color: black; font-size: 15px;">&nbsp;&nbsp;&nbsp;Normal</div>

        <svg width="139" height="20">
          <circle cx="130" cy="10" r="8" fill="red" />
        </svg>
        <div style="color: black; font-size: 15px;">&nbsp;&nbsp;&nbsp;Abnormal</div>

      </div>
      
      <Microservice class="microservice"></Microservice>
    </div>

  </div>

</template>

<script>
import Microservice from '../components/Microservice.vue'
import TimePeriod from '../components/TimePeriod.vue'

export default {
  components: {
    Microservice,
    TimePeriod
  },
  data() {
    return {

    }
  },
  methods: {

  }
}
</script>

<style scoped>
.main {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 96vh;
  margin: 0;
  padding: 0;
}

.left {
  width: 21%;
  height: 100%;
  border-radius: 8px;
}

.LeftMenu {
  height: 100%;
}

.right {
  width: 77%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.microservice {
  height: 100%;
  width: 100%;
}

.circle-container {
  display: flex;
  height: 10vh;
}
</style>
