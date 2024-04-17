<template>
  <div class="left-container">

    <!-- <div class="left-image-box">
      <img class="left-image" src="../assets/logo.png" alt="">
    </div> -->
    <div style="display: flex;margin: 10px 0;">
      <div style="width: 2px;background-color: rgb(88,162,252);"></div>
      <div style="color: black; font-size: 16px;">&nbsp;&nbsp;&nbsp;Task</div>
    </div>

    <div style="display: flex;margin: 24px 0;align-items: center;">
      <div style="color: #516571; font-size: 16px;margin-right: 25px;">&nbsp;&nbsp;&nbsp;&nbsp;Select task</div>
      <select v-model="selectedTask" style="width: 120px; height: 30px; border-radius: 10px; padding: 5px;">
        <!-- <option v-for="(task, index) in taskList" :key="index" :value="task.task_id">{{ task.task_id + ' ' + task.task_name }}</option> -->
        <option value="a">Task 1</option>
        <option value="b">Task 2</option>
        <option value="c">Task 3</option>
      </select>
    </div>

    <div style="display: flex;margin: 10px 0;">
      <div style="width: 2px;background-color: rgb(88,162,252);"></div>
      <div style="color: black; font-size: 16px;">&nbsp;&nbsp;&nbsp;Time period</div>
    </div>
    <div class="menu-box">
      <div class="menu-item" v-for="(period, index) in timePeriods" :key="index">
        <div style="display: flex; justify-content: center;">
          <div style="width: 100%; white-space: nowrap; overflow: hidden; text-align: center;font-size: 14px;">{{
        period.start_time }}
            - {{ period.end_time }}</div>
        </div>
      </div>
    </div>

    <div>

    </div>
    <!-- <div class="export"> -->
      <el-button type="primary" size="mini" @click="downloadTraceCsv" round style="margin-top: 20%;">Export groundtruth</el-button>
    <!-- </div> -->
  </div>

</template>

<script>
import upward from '../assets/upward.svg'
import timePeriodData from '../assets/timeperiod.json'


export default {
  props: {
    traceList: [],
    unlabeled_trace_list: []
  },
  name: 'Manage',
  data() {
    return {
      selectedTimePeriod: '',
      timePeriods: []
    };
  },
  components: {},
  mounted() {
    this.loadTimePeriods();
  },
  methods: {
    loadTimePeriods() {
      this.timePeriods = timePeriodData;
    }
  }
}
</script>

<style>
.left-container {
  height: 100hv;
  color: rgba(255, 255, 255, 1);
  background-color: white;
  font-size: 1.2em;
  border-radius: 8px;
}

.left-image-box {
  width: 80%;
  height: 15%;
  background-color: white;
}

.left-image {
  width: 90%;
  margin: 15px 0;
}

.right {
  width: 81%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.menu-box {
  width: 100%;
  height: 75%;
  overflow-y: auto;
  overflow-x: hidden;
}

.menu-item {
  width: 100%;
  white-space: nowrap;
  /* 不换行 */
  overflow: hidden;
  /* 溢出部分隐藏 */
  font-size: 15px;
  color: #555555;
  background-color: white;
  max-width: 380px;
  padding: 5px 10px;
  line-height: 25px;
  border-bottom: 1px solid #ccc;
  /* border-bottom: 1px solid rgb(54, 90, 123); */
  /* display: flex;
  align-items: center;
  justify-content: center; */
}

.menu-item:hover {
  background-color: rgb(233, 246, 255);
  border-color: rgb(233, 246, 255)
    /* 悬停时将按钮的背景色修改为灰色 */
}


.export {
  /* height: 10%; */
  width: 100%;
  /* display: flex;
  align-items: center; */
  text-align: center;
}

.left-bottom button {
  height: 40px;
}

.el-button {}

.el-button:hover {
  background-color: gray;
  border-color: gray
    /* 悬停时将按钮的背景色修改为灰色 */
}
</style>
