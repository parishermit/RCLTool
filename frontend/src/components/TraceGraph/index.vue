<template>
  <div class="trace-graph">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 15px; border-bottom: 1px solid #eeeeee">
      <div>
        <div class="title">{{spanList[0].operationName}}</div>
        <div class="trace-id">{{id}}</div>
        <div class="detail">
          <label-black value="Start Time"></label-black>
          <div style="margin-right: 10px;">{{spanList[0].startTime}}</div>
          <label-black value="Duration"></label-black>
          <div>{{spanList[0].duration}} ms</div>
        </div>
      </div>
      <div class="tab-list">
        <el-button :type="tabIndex === 0? 'primary': 'info'"
                    @click="() => {this.tabIndex = 0}"
                    icon="el-icon-s-order">List</el-button>
        <el-button :type="tabIndex === 1? 'primary': 'info'"
                    @click="() => {this.tabIndex = 1}"
                    icon="el-icon-s-grid">Grid</el-button>
      </div>
    </div>
    <trace-graph-list v-if="tabIndex === 0"
                      :id="selectedTraceId"></trace-graph-list>
    <trace-graph-table v-if="tabIndex === 1"
                        :spanList="spanList" :id="selectedTraceId"></trace-graph-table>
  </div>
</template>

<script>
import TraceGraphList from '@/components/TraceGraph/list.vue'
import TraceGraphTable from '@/components/TraceGraph/table.vue'
import LabelBlack from '@/components/Label/black.vue'
import { getTrace } from '@/api/trace.js'
import { toHump } from '@/utils/hump-line-convert.js'

export default {
  name: 'TraceGraph',
  components: {
    TraceGraphList,
    TraceGraphTable,
    LabelBlack
  },
  props: {
    id: String
  },
  data () {
    return {
      tabIndex: 0,
      spanList: [],
      selectedTraceId:""
    }
  },
  created () {
    console.log('mounted')
    this.getSpanList().then(() => {
      console.log(this.spanList) // 输出 testList 值
    }).catch((error) => {
      console.error('Error while fetching data:', error)
    })
  },
  methods: {
    getSpanList () {
      return new Promise((resolve, reject) => {
        getTrace({ trace_id: this.id }).then((res) => {
          this.spanList = res.data
          this.spanList.forEach((span) => {
            Object.entries(span).forEach(([key, value]) => {
              delete span[key]
              span[toHump(key)] = value
            })
            span.startTime = new Date(
              Math.round(span.timestamp )
            ).toLocaleString()
          })
          resolve() // 解决 Promise
          // 进行其他操作，如果需要的话
        }).catch((error) => {
          reject(error) // 拒绝 Promise
        })
      })
    }
  },
  watch: {
    id (newVal) {
      console.log('id changed')
      this.selectedTraceId = newVal;
      console.log(this.selectedTraceId);
      this.getSpanList().then(() => {
        console.log('span', this.spanList)
      }).catch((error) => {
        console.error('Error while fetching data:', error)
      })
    }
  }
}
</script>

<style scoped>
.trace-graph {
  padding: 10px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

.trace-id {
  margin-bottom: 10px;
}

.detail {
  display: flex;
  align-items: center;
}

.el-button {
  height: 24px;
  padding: 0px 10px;
}
</style>
