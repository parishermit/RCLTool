<template>
  <el-main style="background-color: #F5F8FA;">
    <div class="main">
      <div class="left">
        <LeftMenu class="LeftMenu" :traceList="traceList" :unlabeled_trace_list="unlabeledTraceList" :sharedValue="sharedValue"
        :type="type"
          @trace-selected="handleTraceSelected"></LeftMenu>
      </div>

      <div class="right">
        <div class="right-top">
          <Topology class="topology" :id="selectedTraceId" @transfer="labelSuccessfully" @update-value="updateValueInB"
          @update-type="updateType"
          ></Topology>
        </div>
        <div class="right-bottom">
          <trace-graph :id="selectedTraceId" />
        </div>
      </div>

    </div>
  </el-main>

</template>

<script>
import LeftMenu from '@/components/LeftMenu.vue'
import Topology from '@/components/Topology.vue'
import TraceGraph from '@/components/TraceGraph/index.vue'
import { getTraceList } from '@/api/trace.js'

export default {
  components: {
    LeftMenu,
    Topology,
    TraceGraph
  },
  data() {
    return {
      traceList: [],
      unlabeledTraceList: [],
      selectedTraceId: '',
      sharedValue:"",
      type:""
    }
  },
  methods: {
    updateValueInB(newValue) {
      this.sharedValue = newValue; // 更新sharedValue的值
    },
    updateType(newValue) {
      this.type = newValue; 
    },
    getTraceList() {
      return new Promise((resolve, reject) => {
        getTraceList().then((res) => {
          this.traceList = res.data
          resolve() // 解决 Promise
          // 进行其他操作，如果需要的话
        }).catch((error) => {
          reject(error) // 拒绝 Promise
        })
      })
    },
    handleTraceSelected(selectedTraceId) {
      this.selectedTraceId = selectedTraceId
      console.log('home select trace id', selectedTraceId)
    },
    labelSuccessfully(labeledTraceId) {
      for (let i = this.traceList.length - 1; i >= 0; i--) {
        if (this.traceList[i] === labeledTraceId) {
          // this.unlabeledTraceList.push(this.traceList.splice(i, 1)[0])
          if (this.traceList.length > 0) {
            this.selectedTraceId =
              this.traceList[Math.floor(Math.random() * this.traceList.length)]
          } else this.selectedTraceId = -1
          break
        }
      }
    }
  },
  created() {
    this.getTraceList().then(() => {
      console.log('tracelist', this.traceList) // 输出 testList 值
    }).catch((error) => {
      console.error('Error while fetching data:', error)
    })
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
  background-color:white;
}

.left {
  width: 18%;
  height: 100%;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;

}

.LeftMenu {
  height: 100%;
}

.right {
  width: 81%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.right-top {
  width: 100%;
  height: 48%;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.topology {
  height: 100%;
  width: 100%;
}

.right-bottom {
  width: 100%;
  height: 48%;
  overflow-y: auto;
  border: 1px rgb(147, 145, 145) solid;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
