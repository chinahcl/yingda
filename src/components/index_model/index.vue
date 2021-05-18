<template>
  <div class="index_11">
    <el-container direction="vertical" style="height:900px;width:100%;">
      <el-header class="index_title"><img src="@/assets/login_t.png" height="100px" >国网小e机器人云服务平台</el-header>
      <el-header class="index_exit">
        <el-col :span="12" :offset="12" style="width:100%;margin:0;text-align: right;padding: 30px 60px 0 0;">
          <span style="width:6.5rem;left:2.5rem;display:inline-block;cursor:pointer;">
            <span style="margin-top:-2rem;">
              <el-dropdown>
                <span style="width:13.5rem;height:2rem; font-size:2px;align:center">
                  {{value1}}
                  <i class="el-icon-arrow-down el-icon--right"></i>
                  <span class="userlogo">
                    <img src="../../assets/login_t.png" alt>
                  </span>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </span>
          </span>
        </el-col>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <Right/>
        </el-aside>
        <!-- <el-main style="height:100%;"> -->
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Right from '@/components/right_list'
export default {
  components: {
    Right
  },
  data () {
    return {
      value1: localStorage.yun_user.replace('"', '').replace('"', '')
    }
  },
  methods: {
    logout () {
      console.log('登出！')
      console.log(localStorage.yun_user)
      console.log('111111')
      localStorage.setItem('yun_user', '')
      localStorage.setItem('grade', '')
      localStorage.setItem('use_unit', '')
      location.reload()
    },
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
.userlogo {
  width: 1.5rem;
  height: 1.5rem;
  display: inline-block;
  line-height: 1rem;
  margin-top: 15px;
  margin-right: 0%;
}
.userlogo img {
  width: 110%;
  height: 110%;
}
.tipboxs span:hover {
  background-color: #e2e0e0;
}
.el-header,
.el-footer {
  background-color: rgb(244, 246, 248);
  color: rgb(187, 178, 178);
  text-align: center;
  font-size: 45px;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: rgb(197, 188, 188);
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: rgb(219, 217, 217);
  text-align: center;
  height: 70%;
  /* line-height: 160px; */
}

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

.el-container{
  background-color: #eee;
}
.el-header{
  height: 120px !important;
  display: block;
  padding: 0;
  background:none;
  border-bottom: 2px solid #ccc;
  box-sizing: border-box;
  margin-bottom: 10px;
}
.index_title{
  width: 775px;
  float: left;
  font-size: 48px;
  line-height: 140px;
    font-weight: bold;
    color: #1f8f8a;
    letter-spacing: 4px;
    text-shadow: #98d9d7 3px 6px 3px;
}
.index_title img{
  display: block;
  float: left;
  padding: 15px 0 0 50px;
}
.index_exit{
    width: calc(100% - 775px);
    float: right;
    position: absolute;
    top: 0;
    right: 0;
}
.el-main{
  background-color: #fff;
}
.el-table{
  font-size: 16px;
  color: #000;
}
.el-submenu.is-active .el-submenu__title {
    border-bottom-color: #1f8f8a;
}
.el-table th>.cell{
  color: #1f8f8a;
  font-size: 20px;
}
.el-table th, .el-table tr{
  background-color: #d8efee;
}
.el-table th, .el-table tr:nth-child(2n){
  background-color: #fff;
}
.el-upload-dragger{
  width: 340px;
}
</style>
