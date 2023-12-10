<template>
  <div class="trace-graph">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 15px; border-bottom: 1px solid #eeeeee">
      <div>
        <div class="title">{{spanList[0].operationName}}</div>
        <div class="trace-id">{{id}}</div>
        <div class="detail">
          <label-black value="Start Time"></label-black>
          <div style="margin-right: 10px;">{{spanList[0].startTime}}</div>
          <label-black value="Duratiob"></label-black>
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
                      :spanList="spanList"></trace-graph-list>
    <trace-graph-table v-if="tabIndex === 1"
                        :spanList="spanList"></trace-graph-table>
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
      spanList: []
    }
  },
  created () {
    console.log('mounted')
    this.getSpanList()
  },
  methods: {
    getSpanList () {
      getTrace({ trace_id: this.id }).then((res) => {
        this.spanList = res.data
        this.spanList.forEach((span) => {
          Object.entries(span).forEach(([key, value]) => {
            delete span[key]
            span[toHump(key)] = value
          })
          span.startTime = new Date(
            Math.round(span.timestamp / 1000)
          ).toLocaleString()
        })
      })
      console.log(this.spanList)
    }
  },
  watch: {
    id () {
      console.log('id changed')
      this.getSpanList()
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
