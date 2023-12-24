<template>
  <div class="trace-graph-table">
    <el-table :data="spanTreeList"
              row-key="spanId"
              border
              default-expand-all
              :tree-props="{children: 'children'}"
              :header-cell-style="{'background-color': '#f3f4f9', 'color': '#2c3e50'}">
      <el-table-column label="Method">
        <template slot-scope="scope">
          <img :src="require('../../assets/' + scope.row.type + '.png')"
                style="margin: 10px 10px -4px 0px" />
          <span :style="{'color': scope.row.statusCode === 200 || scope.row.statusCode === 0? '#2c3e50': '#e54c17'}">{{scope.row.operationName}}</span>
        </template>
      </el-table-column>
      <el-table-column label="Start Time"
                        width="200">
        <template slot-scope="scope">
          <span :style="{'color': scope.row.statusCode === 200 || scope.row.statusCode === 0? '#2c3e50': '#e54c17'}">{{scope.row.startTime}}</span>
        </template>
      </el-table-column>
      <el-table-column label="Duration(ms)"
                        width="100">
        <template slot-scope="scope">
          <span :style="{'color': scope.row.statusCode === 200 || scope.row.statusCode === 0? '#2c3e50': '#e54c17'}">{{scope.row.duration}}</span>
        </template>
      </el-table-column>
      <el-table-column label="Service"
                        width="200">
        <template slot-scope="scope">
          <span :style="{'color': scope.row.statusCode === 200 || scope.row.statusCode === 0? '#2c3e50': '#e54c17'}">{{scope.row.cmdbId}}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'TraceGraphTable',
  props: {
    spanList: Array
  },
  data () {
    return {
      spanTreeList: []
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      this.spanTreeList = this.spanList
      this.spanTreeList.forEach((item) => {
        if (item.parentSpan !== '' && item.parentSpan !== null && item.parentSpan !== undefined) {
          var parentIndex = this.spanTreeList.findIndex(
            (parent) => parent.spanId === item.parentSpan
          )
          if (this.spanTreeList[parentIndex].children === undefined || this.spanTreeList[parentIndex].children === null || this.spanTreeList[parentIndex].children === '') {
            this.spanTreeList[parentIndex].children = [item]
          } else {
            this.spanTreeList[parentIndex].children.push(item)
          }
        }
      })
      this.spanTreeList = this.spanTreeList.filter(
        (span) => span.parentSpan === ''
      )
    }
  },
  watch: {
    spanList () {
      this.getData()
    }
  }
}
</script>

<style scoped>
* {
  font-size: 12px;
}
</style>
