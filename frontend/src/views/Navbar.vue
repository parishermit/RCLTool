<template>
  <div>
    <div style="display: flex;align-items: center;">
      <div style="font-size: 18px;font-weight: bold;width: 21%;">TraceEase</div>
      <div id="NavMenu" style="width: 100%;display: flex;display: flex;justify-content: center">
        <el-menu :default-active="toIndex" class="el-menu-demo" text-color="#000000" active-text-color="#3989fa"
        mode="horizontal" @select="handleSelect">
        <el-menu-item v-for="(item, index) in itemList" :index="item.path" :key="index">
          <span slot="title">{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </div>



    </div>





  <el-main>
      <router-view></router-view>
  </el-main>
  
  
  
  
  </div>

</template>

<script>
export default {
  name: "NavMenu",
  data() {
    return {
      itemList: [    // 水平一级菜单栏的菜单
        { path: '/task', title: 'Task List' },
        { path: '/', title: 'Label anomaly' },
        { path: '/labelrootcause', title: 'Label root cause' },

      ],
    };
  },
  computed: {
    toIndex() {  // 根据路径绑定到对应的一级菜单，防止页面刷新重新跳回第一个
      return '/' + this.$route.path.split('/')[1];
    },
  },
  methods: {
    handleSelect(path) {  // 切换菜单栏
      this.$router.push({
        path: path
      });
    },
  },

};
</script>

<style scoped>
#NavMenu ul{width: 100%;display: flex;justify-content: space-between}
</style>
