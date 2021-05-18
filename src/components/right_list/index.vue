<template>
  <el-scrollbar style="height:70%;">
    <el-menu
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose">
      <!-- <div v-if="editForm == 0"> -->
      <el-submenu index="1" v-if="editForm == '0'">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span>用户自助服务</span>
        </template>
        <el-menu-item-group>
          <el-submenu index="" title="服务单位增加1">
            <template slot="title">服务单位增加</template>
            <el-menu-item index='batch_add_unit' @click="$router.push('/index_1/batch_add_unit')">服务单位增加(批量)</el-menu-item>
            <el-menu-item index='single_add_unit' @click="$router.push('/index_1/single_add_unit')">服务单位增加(单笔)</el-menu-item>
          </el-submenu>
          <el-menu-item index='fronzen_unit' @click="$router.push('/index_1/fronzen_unit')">服务单位冻结</el-menu-item>
          <!-- <el-menu-item index='fronzen_unit' :click="/index_1/fronzen_unit">服务单位冻结</el-menu-item> -->
          <el-menu-item index='thaw_unit' @click="$router.push('/index_1/thaw_unit')">服务单位解冻</el-menu-item>
          <el-menu-item index='query_unit' @click="$router.push('/index_1/query_unit')">服务单位查询</el-menu-item>
          <el-menu-item index='change_unit' @click="$router.push('/index_1/change_unit')">服务单位修改</el-menu-item>
          <el-menu-item index='unit_binding_robot' @click="$router.push('/index_1/unit_binding_robot')">服务单位绑定机器人</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <!-- </div> -->
      <el-submenu index="2" v-if="editForm == '1' | editForm == '0'">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>用户管理</span>
        </template>
                <el-menu-item-group>
          <!-- <el-submenu index="" title="用户增加1"> -->
            <!-- <template slot="title">用户增加</template> -->
            <!-- <el-menu-item index='batch_add_use' @click="$router.push('/index_2/batch_add_use')">用户增加(批量)</el-menu-item> -->
            <el-menu-item index='single_add_use' @click="$router.push('/index_2/single_add_use')">用户增加</el-menu-item>
          <!-- </el-submenu> -->
          <el-menu-item index='fronzen_use' @click="$router.push('/index_2/fronzen_use')">用户冻结</el-menu-item>
          <el-menu-item index='thaw_use' @click="$router.push('/index_2/thaw_use')">用户解冻</el-menu-item>
          <el-menu-item index='query_use' @click="$router.push('/index_2/query_use')">用户查询</el-menu-item>
          <el-menu-item index='change_use' @click="$router.push('/index_2/change_use')">用户修改</el-menu-item>
          <el-menu-item index='use_binding_robot' @click="$router.push('/index_2/use_binding_robot')" v-if="editForm == '1'">用户绑定机器人</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    <!-- </div> -->
    <!-- </div> -->
    <el-submenu index="3" v-if="editForm == '0'">
      <template slot="title">
        <i class="el-icon-menu"></i>
        <span>机器人管理</span>
      </template>
      <el-menu-item-group>
        <!-- <el-submenu index="" title="机器人增加1"> -->
          <!-- <template slot="title">机器人增加</template> -->
          <!-- <el-menu-item index='batch_add_use' @click="$router.push('/index_2/batch_add_use')">用户增加(批量)</el-menu-item> -->
        <el-menu-item index='single_add_robot' @click="$router.push('/robot_manage/single_add_robot')">机器人增加</el-menu-item>
        <!-- </el-submenu> -->
        <el-menu-item index='fronzen_robot' @click="$router.push('/robot_manage/fronzen_robot')">机器人冻结</el-menu-item>
        <el-menu-item index='thaw_robot' @click="$router.push('/robot_manage/thaw_robot')">机器人解冻</el-menu-item>
        <el-menu-item index='query_robot' @click="$router.push('/robot_manage/query_robot')">机器人查询</el-menu-item>
        <el-menu-item index='change_robot' @click="$router.push('/robot_manage/change_robot')">机器人修改</el-menu-item>
        <el-menu-item index='run_state_robot' @click="$router.push('/robot_manage/run_state_robot')">机器人运行状态展示</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <!-- </div> -->
      <el-submenu index="3" v-if="editForm == '2' | editForm == '1'">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>启用机器人</span>
        </template>
        <el-menu-item-group >
          <el-menu-item v-for="(item, index) in robot_list" :key="index" @click="$router.push(item.url)" :index=item.uindex>{{item.name}}</el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-scrollbar>
</template>

<script>
// console.log(this.$store.state.user.id)
export default {
  data () {
    return {
      robot_list: [],
      editForm: ''
      // editFormVisible: this.$store.state.user.id
    }
  },
  created () {
    console.log('localStorage.getItem(user)', localStorage.getItem('yun_user'))
    // const user = localStorage.getItem('user')
    this.editForm = localStorage.getItem('grade')
    this.axios.get('/robotapi/use_get_robot_list/' + localStorage.getItem('yun_user'), {
    }).then(res => {
      console.log(res.data.data)
      this.robot_list = res.data.data
    })
    // this.axios.post('', {})
  },
  // mounted () {
  //   console.log(this.$route.name)
  //   this.active = this.$route.name
  // },
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style>
.el-aside {
display: block;
position: relative;
overflow-y: scroll;
background-color: #eee !important;
width: 260px !important;
}
.el-submenu__title{
    font-size: 20px;
    font-weight: bold;
    color: #1f8f8a;
    border-bottom: 2px solid #1f8f8a;
}
.el-submenu__title i{
  color: #1f8f8a;
}
.el-submenu [class^=el-icon-]{
  font-size: 20px;
}
.el-menu-item, .el-submenu__title{
  height: 66px;
  line-height: 66px;
}
.el-submenu__icon-arrow {
    position: relative;
    top: 0%;
    right: 0;
    margin-top: 0;
    font-size: 20px;
    margin-left: 8px;
}
.el-menu-item-group__title{
  padding: 0;
}
.el-submenu .el-menu-item{
  height: 50px;
  line-height: 50px;
  font-size: 16px;
  color: #333;
}
.el-menu-item:focus, .el-menu-item:hover {
    outline: 0;
    color: #fff !important;
    background-color: #1f8f8a;
}
.el-submenu .el-menu {
    border: none;
    border-bottom: 1px solid #6ec9a1;
}
.el-submenu__title:hover {
    background-color: #ceeae7;
}
.el-menu-item-group>ul li .el-submenu__title{
  font-size: 18px;
  font-weight: normal;
  border-bottom: 1px solid #1f8f8a;
}
.el-menu-item-group>ul li .el-submenu__title {
    font-size: 18px;
    font-weight: normal;
    border-bottom: 1px solid #1f8f8a;
    height: 50px;
    line-height: 50px;
}
</style>
