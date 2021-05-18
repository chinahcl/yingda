<template>
  <header name="logins">
    <el-row>
      <el-col :span="24">
        <div class="grid-content bg-purple-dark" align="center">
          <div class="new_logo">
            <img src="@/assets/login_t.png" height="120px" >
          </div>
          <h1 class="new_title">国网小e机器人云服务平台</h1>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="8">
        <div class="grid-content bg-purple"></div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content bg-purple-light" align="center"></div>
      </el-col>
      <el-col :span="8">
        <div class="grid-content bg-purple"></div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <div class="grid-content bg-purple"></div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content bg-purple-light"></div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6" class="login_warp">
        <div class="grid-content bg-purple">
          <el-form
            :model="ruleForm"
            status-icon
            ref="ruleForm"
            label-width="100px"
            class="demo-ruleForm"
          >
            <el-form-item label="用户名" prop="name">
              <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
              <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <!-- <el-col :span="6">
        <div class="grid-content bg-purple-light"></div>
      </el-col> -->
    </el-row>
    <el-row>
      <el-col :span="4">
        <div class="grid-content bg-purple">
        </div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple-light"></div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple"></div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple-light"></div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple"></div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content bg-purple-light"></div>
      </el-col>
    </el-row>
  </header>
</template>

<script>
import { Message } from 'element-ui'
export default {
  name: 'logins',
  data () {
    // var checkAge = (rule, value, callback) => {
    //   if (!value) {
    //     return callback(new Error('用户名不能为空'))
    //   } else {
    //     callback()
    //   }
    // }
    // var validatePass = (rule, value, callback) => {
    //   if (value === '') {
    //     callback(new Error('请输入密码'))
    //   } else {
    //     callback()
    //   }
    // }
    return {
      ruleForm: {
        pass: '',
        name: ''
      }
    }
  },
  created () {
    console.log('首页')
    // location.reload()
  },
  components: {},
  methods: {
    submitForm () {
      // console.log('发起请求')
      this.axios
        .post('/login_dev/', {
          name: this.ruleForm.name,
          password: this.ruleForm.pass
        })
        .then(res => {
          console.log('res', res.data.code)
          // console.log('xxxxxxx', this.$store.state.user.nm)
          if (res.data.code === 10101) {
            if (res.data.user.is_active === '0') {
              localStorage.setItem('grade', res.data.user.grade)
              localStorage.setItem('use_unit', res.data.user.use_unit)
              Message.success('登陆成功')
              const user = JSON.stringify(res.data.user.userName)
              localStorage.setItem('yun_user', user)
              // this.$store.commit('user/USER_NAME', user)
              // console.log('ssssss', JSON.stringify(this.$store.state.user.nm))
              this.$router.push('/index_1')
            } else {
              Message.warning('用户已冻结')
            }
          } else if (res.data.code === 10102) {
            Message.warning('用户名密码错')
          }
        })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style>
.el-row {
  margin-bottom: 20px;
  /* &:last-child {
    margin-bottom: 0;
  } */
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: rgb(255, 192, 203, -2);
}
.bg-purple {
  background: rgb(255, 192, 203, -2);
}
.bg-purple-light {
  background: rgb(255, 192, 203, -2);
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.new_logo{
  display: block;
  width: 38%;
  float: left;
}
.bg-purple-dark{
  /* padding-top: 6%; */
  width: 100%;
  overflow: hidden;
  }
.new_logo img{
  display: block;
  float: right;
}
.new_title{
  display: block;
  width: 62%;
  float: right;
  font-size: 54px;
  line-height: 52px;
  letter-spacing: 4px;
  color: #048782;
  /* -webkit-box-reflect: below 10px -webkit-linear-gradient(transparent,transparent 50%,rgba(255,255,255,.2)); */
  margin: 0;
  text-shadow: #98d9d7 3px 6px 3px;
  text-align: left;
  text-indent: 1rem;
  padding-top: 50px;
}
.login_warp{
  width: 400px;
  float: none;
  margin: 0 auto;
  box-sizing: border-box;
  padding: 50px 30px 20px;
  box-shadow: 0px 0px 30px #333;
  background-color: #1f8f8a;
  border-radius: 4px;
}
.el-form-item__label{
  display: block !important;
  width: 90px !important;
  float: left !important;
  line-height: 44px !important;
  font-weight: bold !important;
  text-align: right !important;
  white-space: pre !important;
  font-size: 20px !important;
  color: #fff !important;
}
.el-form-item{
  margin-bottom: 25px !important;
}
.el-button{
  background-color: rgba(255,255,255,0);
    font-weight: bold;
    border: 1px solid #fff;
    box-shadow: 0 0 5px #eee;
    border-radius: 0.25em;
    height: 44px;
    font-size: 20px;
    background-color: rgb(255, 255, 255);
    color: #048782;
}
.el-button+.el-button{
  background-color: rgba(255,255,255,0);
  color: #fff;
  margin-left: 20px;
}
.el-button--primary:hover {
    background: #1f8f8a;
    border-color: #1f8f8a;
    color:#fff;
}
.el-button:hover{
  border-color: #1f8f8a;
}
.el-input__inner{
  height: 44px;
  line-height: 44px;
}
</style>
