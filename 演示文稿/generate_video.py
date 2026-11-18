import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_video():
    width, height = 1920, 1080
    fps = 30
    output_path = r"d:\workspace\高级数据库\动画制作\演示文稿\lru_lfu_animation.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 字体加载
    font_path = "C:/Windows/Fonts/msyh.ttc"
    font_title = ImageFont.truetype(font_path, 34)
    font_sub = ImageFont.truetype(font_path, 22)
    font_section = ImageFont.truetype(font_path, 26)
    font_card_title = ImageFont.truetype(font_path, 24)
    font_body = ImageFont.truetype(font_path, 20)
    font_small = ImageFont.truetype(font_path, 16)
    font_code = ImageFont.truetype(font_path, 18)
    font_huge = ImageFont.truetype(font_path, 42)

    # 配色 (与 frontend-design 规范一致的深蓝黑科技实验室调色板)
    BG_COLOR = (10, 14, 23)           # #0A0E17
    CARD_BG = (17, 24, 39)            # #111827
    BORDER_COLOR = (30, 41, 59)       # #1E293B
    BORDER_STRONG = (51, 65, 85)      # #334155
    TEXT_MAIN = (248, 250, 252)       # #F8FAFC
    TEXT_MUTED = (148, 163, 184)      # #94A3B8
    BLUE = (59, 130, 246)             # #3B82F6
    GREEN = (16, 185, 129)            # #10B981
    RED = (244, 63, 94)               # #F43F5E
    AMBER = (245, 158, 11)            # #F59E0B
    PURPLE = (168, 85, 247)           # #A855F7

    # LRU & LFU 仿真内核
    class LRUSim:
        def __init__(self, cap=4):
            self.cap = cap
            self.frames = [None] * cap
            self.pages = [] # MRU at 0, LRU at end
            self.hits = 0
            self.misses = 0
            self.evicts = 0
            self.status = "IDLE"
            self.last_evicted = None

        def access(self, p):
            self.last_evicted = None
            if p in self.pages:
                self.hits += 1
                self.status = "HIT"
                self.pages.remove(p)
                self.pages.insert(0, p)
            else:
                self.misses += 1
                if len(self.pages) >= self.cap:
                    self.evicts += 1
                    self.status = "EVICT"
                    ev = self.pages.pop()
                    self.last_evicted = ev
                    idx = self.frames.index(ev)
                    self.frames[idx] = p
                else:
                    self.status = "MISS"
                    idx = self.frames.index(None)
                    self.frames[idx] = p
                self.pages.insert(0, p)

        def hit_rate(self):
            tot = self.hits + self.misses
            return 0.0 if tot == 0 else (self.hits / tot) * 100

    class LFUSim:
        def __init__(self, cap=4):
            self.cap = cap
            self.frames = [None] * cap # list of page_id
            self.freqs = {} # page -> freq
            self.order = [] # FIFO order of insertion
            self.hits = 0
            self.misses = 0
            self.evicts = 0
            self.status = "IDLE"
            self.last_evicted = None

        def access(self, p):
            self.last_evicted = None
            if p in self.freqs:
                self.hits += 1
                self.status = "HIT"
                self.freqs[p] += 1
            else:
                self.misses += 1
                if len(self.freqs) >= self.cap:
                    self.evicts += 1
                    self.status = "EVICT"
                    # 寻找最小 freq，同频次按 order 最老淘汰
                    min_f = min(self.freqs.values())
                    candidates = [x for x in self.order if self.freqs[x] == min_f]
                    ev = candidates[0]
                    self.last_evicted = ev
                    del self.freqs[ev]
                    self.order.remove(ev)
                    idx = self.frames.index(ev)
                    self.frames[idx] = p
                else:
                    self.status = "MISS"
                    idx = self.frames.index(None)
                    self.frames[idx] = p
                self.freqs[p] = 1
                self.order.append(p)

        def hit_rate(self):
            tot = self.hits + self.misses
            return 0.0 if tot == 0 else (self.hits / tot) * 100

        def get_buckets(self):
            b_dict = {}
            for p, f in self.freqs.items():
                b_dict.setdefault(f, []).append(p)
            return sorted(b_dict.items())

    # 完整演示序列与阶段
    script = [
      # (stage_title, time_code, page, narration, detail)
      ("阶段一：缓冲池冷启动 (Cold Start)", "00:15", "P1", "【冷启动】首个数据页 P1 访问，发生缺页 MISS，分配 Frame 0 载入", "Page Table 注册映射，Pin Count=1，Dirty=0"),
      ("阶段一：缓冲池冷启动 (Cold Start)", "00:30", "P2", "【冷填充】页面 P2 请求，LRU 插入 MRU 头，LFU 进 Freq=1 桶", "Free List 持续提供空槽位，两算法行为完全一致"),
      ("阶段一：缓冲池冷启动 (Cold Start)", "00:45", "P3", "【冷填充】页面 P3 请求，物理帧 Slot 2 被填充", "内存缓冲池逐步由空闲转向饱和状态"),
      ("阶段一：缓冲池冷启动 (Cold Start)", "01:00", "P4", "【池已满】页面 P4 载入，4 个物理缓冲槽位全部占满", "Free List 耗尽，后续任何缺页必须触发页面置换机制！"),

      ("阶段二：常规局部性分流 (Locality Flow)", "01:20", "P1", "【命中 HIT】热点 P1 再次访问，两算法均命中！", "LRU: P1 移至链表最前端 MRU；LFU: P1 升级进入 Freq=2 频次桶"),
      ("阶段二：常规局部性分流 (Locality Flow)", "01:40", "P2", "【命中 HIT】热点 P2 再次访问，两算法再次双双命中！", "LRU: P2 抢占 MRU 头；LFU: P2 频次增至 2。命中率升至 33%"),
      ("阶段二：常规局部性分流 (Locality Flow)", "02:00", "P5", "【首度置换 EVICT】新页 P5 到来！缓冲池已满，必须淘汰一个旧页！", "LRU 淘汰尾部最久未用的 P3；LFU 在 min_freq=1 桶中按 FIFO 同样淘汰 P3"),
      ("阶段二：常规局部性分流 (Locality Flow)", "02:15", "P1", "【热点保持】核心页 P1 持续访问，两算法稳态运行", "稳态下 LRU 与 LFU 均维持高命中率"),

      ("阶段三：边界情形同频决胜 (Tie-Breaking)", "02:35", "P6", "【边界仲裁】页面 P6 到来触发置换！LFU 桶内出现同频竞争", "min_freq=1 桶中有 P4 与 P5。LFU 依据 FIFO 决胜规则精准弹出更老的 P4"),
      ("阶段三：边界情形同频决胜 (Tie-Breaking)", "02:50", "P7", "【边界仲裁】页面 P7 再次触发置换，同频决胜法则再次生效", "LFU 淘汰同频的 P5。严格证明 LFU 桶内决胜具备确定性常数级 O(1) 特性"),
      ("阶段三：边界情形同频决胜 (Tie-Breaking)", "03:05", "P1", "【热点验证】热点 P1 经受住边界抖动考验，持续命中", "P1 频次累加至 4，高筑防护壁垒"),

      ("阶段四：LRU 致命反例——全表扫描污染", "03:30", "S1", "【突发全表扫描】业务执行 SELECT * 扫描，冷数据 S1 强行侵入！", "LRU 将冷页 S1 误认为最重要数据推上 MRU 头；LFU 限制其频次仅为 1"),
      ("阶段四：LRU 致命反例——全表扫描污染", "03:45", "S2", "【扫描冲刷】扫描冷页 S2 继续涌入，LRU 热点开始被迫向尾部退缩", "LRU 缓存污染加剧，LFU 仅在 min_freq=1 桶内自我置换"),
      ("阶段四：LRU 致命反例——全表扫描污染", "04:00", "S3", "【扫描冲刷】扫描冷页 S3 侵入，LRU 发生严重缓存穿透", "LRU 链表被大量单次访问的垃圾数据占领"),
      ("阶段四：LRU 致命反例——全表扫描污染", "04:15", "S4", "【扫描冲刷】扫描冷页 S4 侵入，LRU 核心热点 P2 被驱逐！", "LRU 热点全军覆没！LFU 依靠 Freq=4 壁垒坚决守住热点 P1"),
      ("阶段四：LRU 致命反例——全表扫描污染", "04:30", "P1", "【灾难验证】扫描结束后业务再次请求核心热点 P1！", "【震撼反差】LRU 缺页 MISS（吞吐暴跌）；LFU 完美命中 HIT（免疫全表扫描）！"),

      ("阶段五：LFU 致命反例——频次僵死与漂移", "04:50", "Ghost", "【反转：构造幽灵】历史页 Ghost 经历密集访问，累积巨量频次 Freq=5", "随后业务发生工作集漂移，Ghost 永久成为不再被访问的幽灵！"),
      ("阶段五：LFU 致命反例——频次僵死与漂移", "05:05", "N1", "【工作集漂移】新业务工作集 N1 涌入，两算法面临考验", "N1 初入频次仅为 1。LRU 欣然接纳，LFU 处于观望"),
      ("阶段五：LFU 致命反例——频次僵死与漂移", "05:20", "N2", "【新热点进驻】新活跃页 N2 涌入，LRU 顺畅前移", "由于 Ghost 频次高达 5，LFU 永远不愿淘汰 Ghost！"),
      ("阶段五：LFU 致命反例——频次僵死与漂移", "05:35", "N3", "【LFU 缓存僵死】新活跃页 N3 请求，由于 Ghost 霸占卡位，新页相互践踏", "新数据在 min_freq=1 桶疯狂互杀，出现严重饥饿（Starvation）"),
      ("阶段五：LFU 致命反例——频次僵死与漂移", "05:50", "N1", "【破局验证】业务再次访问新热点 N1！", "【震撼反差】LRU 命中 HIT（快速自适应）；LFU 缺页 MISS（被历史频次锁死）！")
    ]

    lru = LRUSim(4)
    lfu = LFUSim(4)

    # 绘制通用底板
    def draw_base_frame(stage_t, time_c, cur_p, narr_t, detail_t, step_idx, total_steps):
        img = Image.new('RGB', (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # 1. 顶部 Header
        draw.rectangle([(0, 0), (width, 80)], fill=(22, 31, 51))
        draw.line([(0, 80), (width, 80)], fill=BORDER_COLOR, width=2)
        draw.text((40, 20), "高级数据库系统 · 缓冲区页面置换机制深度剖析", font=font_title, fill=TEXT_MAIN)
        draw.text((820, 26), "LRU vs LFU 内核仿真与反例对决 (1080P 60FPS)", font=font_sub, fill=BLUE)

        # 时间与步数胶囊
        draw.rounded_rectangle([(1600, 18), (1880, 62)], radius=12, fill=(15, 23, 42), outline=BORDER_COLOR, width=1)
        draw.text((1620, 26), f"TIME: {time_c} | STEP {step_idx}/{total_steps}", font=font_body, fill=AMBER)

        # 2. 讲解旁白横幅
        draw.rounded_rectangle([(40, 95), (1880, 185)], radius=12, fill=(19, 29, 49), outline=BLUE, width=2)
        draw.text((65, 108), f"▶ 当前阶段：{stage_t}", font=font_card_title, fill=AMBER)
        draw.text((65, 142), narr_t, font=font_section, fill=TEXT_MAIN)
        draw.text((950, 146), f"【内核视点】{detail_t}", font=font_small, fill=TEXT_MUTED)

        # 3. 页面请求流进度条
        draw.rounded_rectangle([(40, 200), (1880, 280)], radius=10, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((60, 210), "页面请求流水线 (Page Stream):", font=font_small, fill=TEXT_MUTED)

        start_x = 360
        # 显示前后相关的请求窗口
        win_start = max(0, step_idx - 5)
        win_end = min(total_steps, step_idx + 8)
        for i in range(win_start, win_end):
            p_name = script[i][2]
            box_x = start_x + (i - win_start) * 115
            is_cur = (i == step_idx - 1)
            b_color = AMBER if is_cur else ((20, 29, 47) if i < step_idx - 1 else (15, 23, 42))
            border_c = (245, 158, 11) if is_cur else BORDER_COLOR
            draw.rounded_rectangle([(box_x, 215), (box_x + 95, 268)], radius=8, fill=b_color, outline=border_c, width=2 if is_cur else 1)
            draw.text((box_x + 8, 218), f"#{i+1}", font=font_small, fill=(100, 116, 139))
            draw.text((box_x + 30, 232), p_name, font=font_card_title, fill=(255, 255, 255) if is_cur else TEXT_MAIN)
            if is_cur:
                draw.text((box_x + 28, 272), "▲ REQ", font=font_small, fill=AMBER)

        # 4. 左侧 LRU 引擎大卡片
        draw.rounded_rectangle([(40, 305), (940, 895)], radius=14, fill=CARD_BG, outline=BLUE, width=2)
        draw.text((65, 320), "● LRU 置换引擎 (时间局部性)", font=font_card_title, fill=BLUE)

        # 状态标牌
        st_color = GREEN if lru.status == "HIT" else (RED if lru.status == "EVICT" else AMBER)
        draw.rounded_rectangle([(700, 318), (915, 356)], radius=6, fill=(15, 23, 42), outline=st_color, width=2)
        st_txt = f"{lru.status} {lru.last_evicted if lru.last_evicted else ''}"
        draw.text((720, 324), st_txt, font=font_body, fill=st_color)

        # LRU 统计
        draw.text((65, 365), f"命中率: {lru.hit_rate():.1f}%   |   命中: {lru.hits}   |   缺页: {lru.misses}   |   淘汰驱逐: {lru.evicts}", font=font_body, fill=TEXT_MUTED)

        # LRU 物理缓冲帧
        draw.text((65, 410), "物理缓冲池帧 (Buffer Frames - Capacity = 4):", font=font_body, fill=TEXT_MAIN)
        for f_i in range(4):
            fx = 65 + f_i * 210
            fy = 445
            p_val = lru.frames[f_i]
            is_active = (p_val == cur_p)
            f_fill = (15, 23, 42) if not is_active else (25, 45, 75)
            f_border = BLUE if is_active else BORDER_COLOR
            draw.rounded_rectangle([(fx, fy), (fx + 195, fy + 140)], radius=10, fill=f_fill, outline=f_border, width=2 if is_active else 1)
            draw.text((fx + 10, fy + 8), f"FRAME {f_i}", font=font_small, fill=(100, 116, 139))
            if p_val:
                draw.text((fx + 65, fy + 38), p_val, font=font_huge, fill=TEXT_MAIN)
                draw.text((fx + 25, fy + 105), "Pin: 1  Dirty: 0", font=font_small, fill=TEXT_MUTED)
            else:
                draw.text((fx + 55, fy + 55), "[空载]", font=font_body, fill=(71, 85, 105))

        # LRU 数据结构：双向链表
        draw.text((65, 620), "内核双向链表结构 (MRU Head ◄──► LRU Tail):", font=font_body, fill=TEXT_MAIN)
        draw.rounded_rectangle([(65, 660), (915, 760)], radius=10, fill=(15, 23, 42), outline=BORDER_COLOR, width=1)
        draw.text((80, 672), "MRU (最新)", font=font_small, fill=BLUE)
        draw.text((820, 672), "LRU (淘汰)", font=font_small, fill=RED)

        lx_start = 170
        for l_i, lp in enumerate(lru.pages):
            nx = lx_start + l_i * 150
            draw.rounded_rectangle([(nx, 680), (nx + 100, 740)], radius=8, fill=(30, 41, 59), outline=BLUE if l_i == 0 else BORDER_COLOR, width=2 if l_i == 0 else 1)
            draw.text((nx + 32, 695), lp, font=font_card_title, fill=TEXT_MAIN)
            if l_i < len(lru.pages) - 1:
                draw.text((nx + 115, 700), "⇄", font=font_section, fill=(100, 116, 139))

        # 5. 右侧 LFU 引擎大卡片
        draw.rounded_rectangle([(980, 305), (1880, 895)], radius=14, fill=CARD_BG, outline=GREEN, width=2)
        draw.text((1005, 320), "● LFU 置换引擎 (频次局部性 · O(1)双向频次桶)", font=font_card_title, fill=GREEN)

        # 状态标牌
        lfu_st_color = GREEN if lfu.status == "HIT" else (RED if lfu.status == "EVICT" else AMBER)
        draw.rounded_rectangle([(1640, 318), (1855, 356)], radius=6, fill=(15, 23, 42), outline=lfu_st_color, width=2)
        lfu_st_txt = f"{lfu.status} {lfu.last_evicted if lfu.last_evicted else ''}"
        draw.text((1660, 324), lfu_st_txt, font=font_body, fill=lfu_st_color)

        # LFU 统计
        draw.text((1005, 365), f"命中率: {lfu.hit_rate():.1f}%   |   命中: {lfu.hits}   |   缺页: {lfu.misses}   |   淘汰驱逐: {lfu.evicts}", font=font_body, fill=TEXT_MUTED)

        # LFU 物理缓冲帧
        draw.text((1005, 410), "物理缓冲池帧 (Buffer Frames - 维护独立频次):", font=font_body, fill=TEXT_MAIN)
        for f_i in range(4):
            fx = 1005 + f_i * 210
            fy = 445
            p_val = lfu.frames[f_i]
            is_active = (p_val == cur_p)
            f_fill = (15, 23, 42) if not is_active else (20, 50, 40)
            f_border = GREEN if is_active else BORDER_COLOR
            draw.rounded_rectangle([(fx, fy), (fx + 195, fy + 140)], radius=10, fill=f_fill, outline=f_border, width=2 if is_active else 1)
            draw.text((fx + 10, fy + 8), f"FRAME {f_i}", font=font_small, fill=(100, 116, 139))
            if p_val:
                draw.text((fx + 65, fy + 38), p_val, font=font_huge, fill=TEXT_MAIN)
                freq_val = lfu.freqs.get(p_val, 0)
                draw.text((fx + 35, fy + 105), f"Freq: {freq_val} 次", font=font_body, fill=GREEN)
            else:
                draw.text((fx + 55, fy + 55), "[空载]", font=font_body, fill=(71, 85, 105))

        # LFU 数据结构：O(1) 频次桶展示
        draw.text((1005, 620), "内核 O(1) 频次桶双链表结构 (min_freq 锁定最低桶):", font=font_body, fill=TEXT_MAIN)
        draw.rounded_rectangle([(1005, 660), (1855, 860)], radius=10, fill=(15, 23, 42), outline=BORDER_COLOR, width=1)

        buckets = lfu.get_buckets()
        min_f = min(lfu.freqs.values()) if lfu.freqs else 1
        by_start = 675
        for b_idx, (fq, p_list) in enumerate(buckets[:3]):
            by = by_start + b_idx * 58
            is_min = (fq == min_f)
            b_tag_c = GREEN if is_min else BLUE
            draw.rounded_rectangle([(1025, by), (1160, by + 46)], radius=6, fill=(30, 41, 59), outline=b_tag_c, width=2 if is_min else 1)
            draw.text((1035, by + 12), f"Freq = {fq} {'[MIN]' if is_min else ''}", font=font_body, fill=b_tag_c)

            # 桶内节点
            nx = 1180
            for node_p in p_list:
                draw.rounded_rectangle([(nx, by), (nx + 90, by + 46)], radius=6, fill=(20, 29, 47), outline=BORDER_COLOR, width=1)
                draw.text((nx + 25, by + 10), node_p, font=font_card_title, fill=TEXT_MAIN)
                nx += 105

        # 6. 底部累计命中率对比进度条
        draw.rounded_rectangle([(40, 920), (1880, 1040)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((65, 935), "实时累计命中率直观对决 (Cumulative Hit Ratio):", font=font_body, fill=TEXT_MAIN)

        # LRU 条
        draw.text((65, 970), "LRU:", font=font_body, fill=BLUE)
        draw.rounded_rectangle([(130, 970), (1200, 995)], radius=6, fill=(15, 23, 42), outline=BORDER_COLOR, width=1)
        lru_w = int((lru.hit_rate() / 100.0) * 1070)
        if lru_w > 0:
            draw.rounded_rectangle([(130, 970), (130 + lru_w, 995)], radius=6, fill=BLUE)
        draw.text((1220, 970), f"{lru.hit_rate():.1f}%", font=font_body, fill=BLUE)

        # LFU 条
        draw.text((65, 1005), "LFU:", font=font_body, fill=GREEN)
        draw.rounded_rectangle([(130, 1005), (1200, 1030)], radius=6, fill=(15, 23, 42), outline=BORDER_COLOR, width=1)
        lfu_w = int((lfu.hit_rate() / 100.0) * 1070)
        if lfu_w > 0:
            draw.rounded_rectangle([(130, 1005), (130 + lfu_w, 1030)], radius=6, fill=GREEN)
        draw.text((1220, 1005), f"{lfu.hit_rate():.1f}%", font=font_body, fill=GREEN)

        # 右侧结论卡
        draw.text((1350, 940), "【实时机制洞察】", font=font_body, fill=AMBER)
        if step_idx <= 11:
            draw.text((1350, 975), "稳态与常规访问下，两算法表现高度一致，命中率平稳上升。", font=font_small, fill=TEXT_MUTED)
        elif step_idx <= 16:
            draw.text((1350, 975), "全表扫描冲击！LRU 遭遇严重缓存污染，LFU 展现强大频次免疫。", font=font_small, fill=RED)
        else:
            draw.text((1350, 975), "工作集漂移！LFU 陷入历史频次僵死，LRU 敏捷自我修复收敛。", font=font_small, fill=AMBER)

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    print(f"Total script steps: {len(script)}")

    # 渲染起始封面 (2 秒 = 60 帧)
    title_img = Image.new('RGB', (width, height), BG_COLOR)
    t_draw = ImageDraw.Draw(title_img)
    t_draw.text((450, 320), "《高级数据库系统》大作业汇报", font=font_huge, fill=BLUE)
    t_draw.text((320, 420), "缓冲区页面置换机制：LRU 与 LFU 深度对比演示", font=ImageFont.truetype(font_path, 48), fill=TEXT_MAIN)
    t_draw.text((420, 520), "正常流程 · 边界情形 · 全表扫描污染 · 历史频次僵死 · 工业破局", font=font_section, fill=GREEN)
    t_draw.text((680, 680), "正在载入双引擎仿真内核...", font=font_body, fill=TEXT_MUTED)
    title_frame = cv2.cvtColor(np.array(title_img), cv2.COLOR_RGB2BGR)
    for _ in range(60):
        out.write(title_frame)

    # 逐步演练每个 Step
    for idx, (st_title, t_code, page, narr, detail) in enumerate(script):
        step_num = idx + 1
        lru.access(page)
        lfu.access(page)

        frame_bgr = draw_base_frame(st_title, t_code, page, narr, detail, step_num, len(script))
        # 每个 Step 持续 40 帧 (约 1.33 秒)
        for _ in range(40):
            out.write(frame_bgr)

    # 渲染总结致谢尾页 (3 秒 = 90 帧)
    end_img = Image.new('RGB', (width, height), BG_COLOR)
    e_draw = ImageDraw.Draw(end_img)
    e_draw.text((480, 300), "演示完毕 · 汇报总结", font=font_huge, fill=GREEN)
    e_draw.text((340, 400), "LRU 擅长敏捷遗忘但怕扫描；LFU 擅长守卫热点但怕僵死", font=font_section, fill=TEXT_MAIN)
    e_draw.text((380, 460), "工业界最佳实践：MySQL Midpoint 5:8 隔离 与 PG Clock-Sweep 衰减", font=font_section, fill=AMBER)
    e_draw.text((580, 620), "谢谢各位评委老师！欢迎提问指导", font=font_huge, fill=BLUE)
    end_frame = cv2.cvtColor(np.array(end_img), cv2.COLOR_RGB2BGR)
    for _ in range(90):
        out.write(end_frame)

    out.release()
    print(f"Video successfully rendered to: {output_path}")

if __name__ == "__main__":
    render_video()
