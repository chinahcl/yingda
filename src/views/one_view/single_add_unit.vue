<template>
  <div id="sigle_add_unit">
    <el-row>
  <el-col :span="2"><div class="grid-content bg-purple" style="background:transparent"></div></el-col>
  <el-col :span="19"><div class="grid-content bg-purple-light" style="background:transparent">
    <el-form :model="ruleForm" status-icon ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <table border="0">
    <th colspan="2">服务单位信息增加</th>
  <tr>
    <td><el-form-item label="单位名称" prop="unit_name">
    <el-input v-model="ruleForm.unit_name"></el-input>
  </el-form-item></td>
    <td><el-form-item label="单位简称" prop="unit_abb">
    <el-input v-model="ruleForm.unit_abb"></el-input>
  </el-form-item></td>
  </tr>
  <tr>
    <td><el-form-item label="联系人" prop="use">
    <el-input v-model="ruleForm.use"></el-input>
  </el-form-item></td>
    <td><el-form-item label="联系电话" prop="phone">
    <el-input v-model="ruleForm.phone"></el-input>
  </el-form-item></td>
  </tr>
    <tr>
    <td><el-form-item label="手机号" prop="iphone">
    <el-input v-model="ruleForm.iphone"></el-input>
  </el-form-item></td>
    <!-- <td><el-form-item label="活动名称">
    <el-input v-model="form.name"></el-input>
  </el-form-item></td> -->
  </tr>
    <tr>
    <td><el-form-item label="办公地址" prop="address">
    <el-input v-model="ruleForm.address" style="width:240%"></el-input>
  </el-form-item></td>
  </tr>
  <tr>
    <td><div style="margin-right:-120px"><el-button type="primary"  @click="submitForm('ruleForm')">提交</el-button></div></td>
    <td><div style="margin-left:-120px"><el-button type="info" @click="resetForm('ruleForm')">重置</el-button></div></td>
  </tr>
</table>
</el-form>
    </div></el-col>
  <el-col :span="3"><div class="grid-content bg-purple" style="background:transparent"></div></el-col>
</el-row>
  </div>
</template>

<script>
import { Message } from 'element-ui'
export default {
  name: 'sigle_add_unit',
  data () {
    return {
      ruleForm: {
        unit_name: '',
        unit_abb: '',
        use: '',
        phone: '',
        iphone: '',
        address: '',
        userxu: '1',
        uintstate: 1,
        name: localStorage.yun_user.replace('"', '').replace('"', '')
      }
    }
  },
  methods: {
    submitForm (formName) {
      console.log(formName.unit_name)
      const data = this.ruleForm
      this.axios.post('/users', {
        data
      }).then((res) => {
        if (res.data.code === 1) {
          Message.success('增加成功')
          // this.tableData = res.data.data
          console.log(res.data)
          this.$refs[formName].resetFields()
        } else {
          Message.warning('重复账号')
        }
      }).catch((error) => {
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
#sigle_add_unit {
  margin-top: 20px
}
h5 {
    line-height: 1px;
    color:black;
    font-size: 22px
}
th {
  border-top:100cm;
  line-height: 1px;
  color: #0e0d0d;
  font-size :22px
}
</style>
