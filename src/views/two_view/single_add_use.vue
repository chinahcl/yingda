<template>
  <div id="sigle_add_use">
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
              <th colspan="2">用户信息增加</th>
              <tr>
                <td>
                  <el-form-item label="姓名(账号)" prop="u_name">
                    <el-input v-model="ruleForm.u_name"></el-input>
                  </el-form-item>
                </td>
                <td>
                  <el-form-item label="单位名称">
                    <el-select v-model="ruleForm.use_unit" placeholder>
                      <el-option
                        v-for="(item,index) in options"
                        :key="index"
                        :label="item.label"
                        :value="item.value"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </td>
              </tr>
              <tr>
                <td>
                  <el-form-item label="身份证号" prop="use_id">
                    <el-input v-model="ruleForm.use_id"></el-input>
                  </el-form-item>
                </td>
                <td>
                  <el-form-item label="部门" prop="ment">
                    <el-input v-model="ruleForm.ment"></el-input>
                  </el-form-item>
                </td>
              </tr>
              <tr>
                <td>
                  <el-form-item label="办公电话" prop="unit_phone">
                    <el-input v-model="ruleForm.unit_phone"></el-input>
                  </el-form-item>
                </td>
                <td>
                  <el-form-item label="处室名称" prop="chu_name">
                    <el-input v-model="ruleForm.chu_name"></el-input>
                  </el-form-item>
                </td>
              </tr>
              <tr>
                <td>
                  <el-form-item label="手机" prop="use_iphone">
                    <el-input v-model="ruleForm.use_iphone" oninput ="value=value.replace(/[^\d]/g,'')"></el-input>
                  </el-form-item>
                </td>
                <td>
                  <el-form-item label="密码" prop="password">
                    <el-input v-model="ruleForm.password"></el-input>
                  </el-form-item>
                </td>
              </tr>
              <tr>
                <td>
                  <el-form-item label="办公地址" prop="use_address">
                    <el-input v-model="ruleForm.use_address" style="width:240%"></el-input>
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
  data () {
    return {
      options: [],
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      ruleForm: {
        u_name: '',
        use_unit: '',
        use_id: '',
        ment: '',
        unit_phone: '',
        chu_name: '',
        use_iphone: '',
        use_address: '',
        password: '',
        grade: localStorage.yun_user.replace('"', '').replace('"', '')
      }
    }
  },
  created () {
    const id = localStorage.use_unit
    this.axios.get('/users/unit_name/' + id, {}).then(res => {
      this.options = res.data.data
    })
  },
  methods: {
    submitForm (formName) {
      console.log(formName.u_name)
      const data = this.ruleForm
      const name = this.name
      this.axios.post('/login_dev/reight', {
        data,
        name
      }).then(res => {
        if (res.data.code === 1) {
          Message.success('增加成功')
          // this.tableData = res.data.data
          console.log(res.data)
          this.$refs[formName].resetFields()
        } else {
          Message.warning('账号或身份证号或手机号重复')
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

<style>
#sigle_add_unit {
  margin-top: 20px;
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
.el-form-item__label{
  color:black !important;
}
</style>
