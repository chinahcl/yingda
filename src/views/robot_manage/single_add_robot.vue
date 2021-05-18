<template>
  <div id="sigle_add_robot">
    <el-row>
      <el-col :span="2">
        <div class="grid-content bg-purple" style="background:transparent"></div>
      </el-col>
      <el-col :span="19">
        <div class="grid-content bg-purple-light" style="background:transparent">
          <el-form
            :model="ruleForm"
            status-icon
            ref="ruleForm"
            label-width="100px"
            class="demo-ruleForm"
          >
            <table border="0">
              <th colspan="2">机器人信息增加</th>
              <tr>
                <td>
                  <el-form-item label="机器人名称" prop="robot_name">
                    <el-input v-model="ruleForm.robot_name"></el-input>
                  </el-form-item>
                </td>
                <td>
                  <el-form-item label="机器人路径" prop="robot_path">
                    <el-input v-model="ruleForm.robot_path"></el-input>
                  </el-form-item>
                </td>
              </tr>
              <tr>
                <td>
                  <div style="margin-right:-120px">
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                  </div>
                </td>
                <td>
                  <div style="margin-left:-120px">
                    <el-button type="info" @click="resetForm('ruleForm')">重置</el-button>
                  </div>
                </td>
              </tr>
            </table>
          </el-form>
        </div>
      </el-col>
      <el-col :span="3">
        <div class="grid-content bg-purple" style="background:transparent"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { Message } from 'element-ui'
export default {
  // name: 'single_add_robot',
  data () {
    return {
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      ruleForm: {
        robot_name: '',
        robot_path: '/robot/'
      }
    }
  },
  methods: {
    submitForm (formName) {
      // console.log('formName.robot_name')
      const data = this.ruleForm
      console.log(data)
      const id = localStorage.use_unit
      const name = this.name
      this.axios.post('/robotapi/' + id, {
        data,
        name
      })
        .then(res => {
          if (res.data.code === 1) {
            Message.success('增加成功')
            // this.tableData = res.data.data
            console.log(res.data)
            this.$refs[formName].resetFields()
          } else {
            Message.warning('重复账号')
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    resetForm (formName) {
      console.log('reset!')
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style scoped>
#sigle_add_robot {
  margin-top: 30px;
}
h5 {
  line-height: 1px;
  color: #0e0d0d;
  font-size: 22px;
}
th {
  border-top: 100cm;
  line-height: 1px;
  color: black;
  font-size: 22px;
}
</style>
