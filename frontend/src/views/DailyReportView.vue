<template>
  <div class="page-stack">
    <section class="toolbar-panel">
      <label>
        报告日期
        <input v-model="reportDate" type="date" @change="loadData" />
      </label>
    </section>

    <section class="stats-grid">
      <StatCard label="新增会员" :value="report.new_members.count" hint="今日注册会员数" :icon="UserPlus" />
      <StatCard label="积分兑换" :value="report.redeems.count" :hint="'消耗 ' + report.redeems.total_points + ' 积分'" :icon="Gift" />
      <StatCard label="预售订单" :value="report.presales.order_count" :hint="'￥' + report.presales.total_amount + ' / ' + report.presales.total_quantity + '份'" :icon="ShoppingBag" />
      <StatCard label="推荐鲜果" :value="report.recommendations.count" hint="今日推荐清单" :icon="Sprout" />
    </section>

    <div class="content-grid two-columns">
      <section class="panel">
        <div class="panel-header">
          <h2>新增会员</h2>
        </div>
        <div class="rank-list">
          <article v-for="member in report.new_members.items" :key="member.id" class="rank-item">
            <div>
              <strong>{{ member.name }}</strong>
              <span>{{ member.phone }} · 等级 {{ member.level_id }}</span>
            </div>
            <span>{{ member.created_at }}</span>
          </article>
        </div>
        <EmptyState v-if="!report.new_members.items.length" text="今日无新增会员" />
      </section>

      <section class="panel">
        <div class="panel-header">
          <h2>积分兑换</h2>
        </div>
        <div class="rank-list">
          <article v-for="record in report.redeems.items" :key="record.id" class="rank-item">
            <div>
              <strong>{{ record.member_name }}</strong>
              <span>{{ record.note }}</span>
            </div>
            <b class="negative">{{ record.change }} 分</b>
          </article>
        </div>
        <EmptyState v-if="!report.redeems.items.length" text="今日无兑换记录" />
      </section>
    </div>

    <div class="content-grid two-columns">
      <section class="panel">
        <div class="panel-header">
          <h2>预售订单</h2>
        </div>
        <div class="rank-list">
          <article v-for="order in report.presales.items" :key="order.id" class="rank-item">
            <div>
              <strong>{{ order.presale_title }}</strong>
              <span>{{ order.member_name }} · {{ order.created_at }}</span>
            </div>
            <b>￥{{ order.amount }} / {{ order.quantity }}份</b>
          </article>
        </div>
        <EmptyState v-if="!report.presales.items.length" text="今日无预售订单" />
      </section>

      <section class="panel">
        <div class="panel-header">
          <h2>今日鲜果推荐</h2>
        </div>
        <div class="recommendation-grid">
          <article v-for="fruit in report.recommendations.items" :key="fruit.id" class="fruit-card">
            <div class="fruit-visual">{{ fruit.name.slice(0, 1) }}</div>
            <div class="fruit-body">
              <div>
                <strong>{{ fruit.name }}</strong>
                <span>{{ fruit.origin }} · {{ fruit.category }}</span>
              </div>
              <b class="price-label">￥{{ fruit.price }} · 新鲜度 {{ fruit.freshness_score }}</b>
              <p>{{ fruit.reason }}</p>
            </div>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Gift, ShoppingBag, Sprout, UserPlus } from 'lucide-vue-next'

import { fallbackDailyReport } from '../api/fallback'
import { dailyReportApi } from '../api/dailyReport'
import EmptyState from '../components/EmptyState.vue'
import StatCard from '../components/StatCard.vue'

const today = new Date().toISOString().slice(0, 10)
const reportDate = ref(today)
const report = ref({ ...fallbackDailyReport })

async function loadData() {
  const data = await dailyReportApi.get(reportDate.value).catch(() => fallbackDailyReport)
  if (data) report.value = data
}

onMounted(loadData)
</script>
