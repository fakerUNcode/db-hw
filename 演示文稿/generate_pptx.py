import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 宽屏尺寸
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # 配色方案 (符合 frontend-design 规范的现代系统实验室配色)
    COLOR_BG = RGBColor(10, 14, 23)       # 深蓝黑 #0A0E17
    COLOR_CARD = RGBColor(17, 24, 39)     # 板岩深灰 #111827
    COLOR_BORDER = RGBColor(30, 41, 59)   # 极细边框 #1E293B
    COLOR_BORDER_STRONG = RGBColor(51, 65, 85) # 强化边框 #334155
    COLOR_TEXT = RGBColor(248, 250, 252)  # 珍珠白 #F8FAFC
    COLOR_MUTED = RGBColor(148, 163, 184) # 科技灰 #94A3B8
    COLOR_BLUE = RGBColor(59, 130, 246)   # 科技蓝 #3B82F6
    COLOR_GREEN = RGBColor(16, 185, 129)  # 翠绿 #10B981
    COLOR_RED = RGBColor(244, 63, 94)     # 警戒玫瑰红 #F43F5E
    COLOR_AMBER = RGBColor(245, 158, 11)  # 琥珀金 #F59E0B
    COLOR_PURPLE = RGBColor(168, 85, 247) # 破局紫 #A855F7

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="《高级数据库系统》内核算法动画与研讨"):
        # 顶部标签
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_BLUE

        # 标题文本
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT

        # 顶部分隔线
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, title="", border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.color.rgb = COLOR_BORDER
            card.line.width = Pt(1)

        if title:
            # 标题条
            title_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), Inches(0.4))
            tf = title_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            if border_color:
                p.font.color.rgb = border_color
            else:
                p.font.color.rgb = COLOR_TEXT
        return card

    # ==========================================
    # SLIDE 1: 封面
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # 封面装饰发光框
    decor = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    decor.fill.solid()
    decor.fill.fore_color.rgb = COLOR_BLUE
    decor.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "《高级数据库系统》大作业 · 动画报告与理论研讨"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_BLUE
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "缓冲区页面置换机制深度剖析"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT

    p2 = tf1.add_paragraph()
    p2.text = "LRU 与 LFU 的内核对比、边界反例及现代工业破局演化"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_GREEN
    p2.space_before = Pt(8)
    p2.space_after = Pt(18)

    p3 = tf1.add_paragraph()
    p3.text = "教师选题：围绕缓冲内容、最近访问次序、频次、命中与淘汰对象等，深度剖析置换内核与反例。"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_MUTED

    # 底部作者与信息卡片
    info_card = add_card(s1, Inches(1.2), Inches(4.8), Inches(10.9), Inches(1.8))
    info_box = s1.shapes.add_textbox(Inches(1.4), Inches(4.9), Inches(10.5), Inches(1.6))
    itf = info_box.text_frame
    itf.word_wrap = True

    ip1 = itf.paragraphs[0]
    ip1.text = "答辩小组分工：全组共 3 人  |  答辩时长：5分钟讲解 + 现场问答  |  考核目标：满分标准交付"
    ip1.font.size = Pt(13)
    ip1.font.bold = True
    ip1.font.color.rgb = COLOR_TEXT
    ip1.space_after = Pt(8)

    ip2 = itf.add_paragraph()
    ip2.text = "• 组长 / 内核机制主讲：全面统筹机制剖析、算法形式化证明、全表扫描与缓存僵死反例论证\n• 组员一 / 动画系统研发：构建 HTML5/SVG 双引擎交互动画仿真平台、页面请求流与状态机调度\n• 组员二 / 工业演化与问答：PostgreSQL Clock 与 MySQL InnoDB Midpoint 机制落地及答辩 Q&A"
    ip2.font.size = Pt(11)
    ip2.font.color.rgb = COLOR_MUTED

    s1.notes_slide.notes_text_frame.text = "各位老师、评委同学好！今天我们小组汇报的课题是《缓冲区页面置换机制：LRU与LFU的内核对比与演进》。我们将通过深度理论推演与5分钟高保真交互动画，系统展现正常过程、边界情形及致命反例，并拓展至现代数据库真实内核。"

    # ==========================================
    # SLIDE 2: 缓冲池体系结构
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "01. 存储引擎中枢：缓冲池 (Buffer Pool) 的架构与核心命题")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "缓冲池核心定位与鸿沟", COLOR_BLUE)
    c1_box = s2.shapes.add_textbox(Inches(0.95), Inches(2.2), Inches(3.3), Inches(4.4))
    tf_c1 = c1_box.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "磁盘 I/O 与内存的巨大鸿沟"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    bullets1 = [
      "内存访问时延约为 50~100 ns，而 NVMe SSD 寻址约为 10~50 μs（慢近 1000 倍），机械硬盘达毫秒级。",
      "Buffer Pool 扮演内存与物理外存的枢纽，将热点数据常驻以消除昂贵磁盘 I/O。",
      "容量严格受限：数据量远大于物理内存，因此页面置换（Eviction）算法决定了数据库吞吐量上限。"
    ]
    for b in bullets1:
        p = tf_c1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(8)

    add_card(s2, Inches(4.7), Inches(1.6), Inches(4.2), Inches(5.2), "缓冲池内核关键构成组件", COLOR_GREEN)
    c2_box = s2.shapes.add_textbox(Inches(4.85), Inches(2.2), Inches(3.9), Inches(4.4))
    tf_c2 = c2_box.text_frame
    tf_c2.word_wrap = True

    components = [
      ("Page Table (映射散列表)", "实现 page_id 到 frame_id 的 O(1) 快速寻址。未命中时发生缺页。"),
      ("Buffer Frames (物理帧槽)", "内存连续大数组，用于容纳 4KB/8KB/16KB 物理页实体数据。"),
      ("Pin Count (引用计数/Pin锁)", "跟踪当前正访问该帧的并发事务线程。Pin > 0 绝对禁止驱逐！"),
      ("Dirty Flag & WAL 约束", "置换脏页前必须遵循 Write-Ahead Logging (WAL) 协议先将日志刷盘，再将脏页写回。")
    ]
    for idx, (head, desc) in enumerate(components):
        p = tf_c2.paragraphs[0] if idx == 0 else tf_c2.add_paragraph()
        p.text = f"{idx+1}. {head}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT

        p_desc = tf_c2.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = COLOR_MUTED
        p_desc.space_after = Pt(8)

    add_card(s2, Inches(9.2), Inches(1.6), Inches(3.3), Inches(5.2), "置换算法的核心考核准则", COLOR_AMBER)
    c3_box = s2.shapes.add_textbox(Inches(9.35), Inches(2.2), Inches(3.0), Inches(4.4))
    tf_c3 = c3_box.text_frame
    tf_c3.word_wrap = True

    criteria = [
      ("最大化命中率 (Hit Rate)", "Hit = 命中，Miss = 缺页。在真实 OLTP 业务中，命中率从 95% 提升到 99%，磁盘 I/O 暴降 80%！"),
      ("严格 O(1) 时间复杂度", "每次查询请求必须在常数时间内判定命中、移动指针或执行淘汰，不得出现 O(N) 链表遍历。"),
      ("极低并发锁开销 (Scalability)", "在高并发多核处理器下，尽量减少全局大锁争用，支持高吞吐并发读写。")
    ]
    for idx, (head, desc) in enumerate(criteria):
        p = tf_c3.paragraphs[0] if idx == 0 else tf_c3.add_paragraph()
        p.text = f"★ {head}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_AMBER

        p_desc = tf_c3.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = COLOR_MUTED
        p_desc.space_after = Pt(10)

    s2.notes_slide.notes_text_frame.text = "在深入算法前，我们先建立存储引擎的全局视点：缓冲池由 Page Table、Buffer Frames、Pin Count 和 Dirty Flag 组成。置换算法的目标是用 O(1) 极简开销将命中率推向极致。"

    # ==========================================
    # SLIDE 3: LRU 机制深度剖析
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "02. LRU (Least Recently Used) 机制剖析：时间局部性与 O(1) 双链表")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "LRU 核心哲学与状态机", COLOR_BLUE)
    box3_1 = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf3_1 = box3_1.text_frame
    tf3_1.word_wrap = True

    p = tf3_1.paragraphs[0]
    p.text = "时间局部性假设 (Temporal Locality)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    p2 = tf3_1.add_paragraph()
    p2.text = "如果一个页面刚刚被访问过，那么它在不久的将来大概率会再次被访问；反之，越久未被引用的页面，未来被访问的概率越低。"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_after = Pt(12)

    p3 = tf3_1.add_paragraph()
    p3.text = "标准置换操作流程："
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_BLUE

    steps_lru = [
      ("命中 (Hit)", "Hash Map 定位节点 -> 将其从当前双链表位置断开 -> 插入 MRU 头部 (O(1))。"),
      ("未命中且未满 (Miss & Insert)", "分配空闲 Frame -> 创建节点挂载至 MRU 头部 -> Hash Map 注册 (O(1))。"),
      ("未命中且已满 (Miss & Evict)", "直接从 LRU 尾部弹出节点（确保 Pin=0）-> 驱逐并从 Hash Map 注销 -> 新页挂载至 MRU 头部 (O(1))。")
    ]
    for s_title, s_desc in steps_lru:
        p = tf3_1.add_paragraph()
        p.text = f"• {s_title}: {s_desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "工业级 O(1) 双向链表 + 哈希表结构", COLOR_BLUE)
    box3_2 = s3.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf3_2 = box3_2.text_frame
    tf3_2.word_wrap = True

    p = tf3_2.paragraphs[0]
    p.text = "数据结构图解与拓扑关系"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(8)

    diag_text = (
      "[ Page Table: Hash Map ]\n"
      "   Page_ID ──► (Pointer to Doubly Linked Node)\n\n"
      "[ Doubly Linked List ]\n"
      "   ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐\n"
      "   │ MRU HEAD│ ◄──► │ Page P1 │ ◄──► │ Page P2 │ ◄──► │ LRU TAIL│\n"
      "   └─────────┘      └─────────┘      └─────────┘      └─────────┘\n"
      "   (最新访问插入)                                    (最优先驱逐淘汰)"
    )
    p_diag = tf3_2.add_paragraph()
    p_diag.text = diag_text
    p_diag.font.size = Pt(10)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_BLUE
    p_diag.space_after = Pt(12)

    analysis_lru = [
      ("空间复杂度", "O(N)，每个缓冲帧需额外存储 prev 与 next 双向指针。"),
      ("时间复杂度", "命中、插入与驱逐均为严格 O(1)。"),
      ("并发致命伤", "每次读写命中都必须对全局链表进行指针摘除和头部插入，必须持有全局互斥锁（Mutex/Latch），多线程竞争极其剧烈！")
    ]
    for a_t, a_d in analysis_lru:
        p = tf3_2.add_paragraph()
        p.text = f"• {a_t}：{a_d}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(4)

    s3.notes_slide.notes_text_frame.text = "LRU 的核心依托时间局部性，通过哈希表加双向链表实现 O(1) 的命中移动与尾部淘汰。但大家请注意最后一条：LRU 每次读命中都必须修改链表指针，这在多核高并发数据库中是巨大的锁争用隐患。"

    # ==========================================
    # SLIDE 4: LFU 机制深度剖析
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "03. LFU (Least Frequently Used) 机制剖析：频次局部性与 O(1) 桶设计")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "LFU 核心哲学与传统陷阱", COLOR_GREEN)
    box4_1 = s4.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf4_1 = box4_1.text_frame
    tf4_1.word_wrap = True

    p = tf4_1.paragraphs[0]
    p.text = "频次局部性假设 (Frequency Locality)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    p2 = tf4_1.add_paragraph()
    p2.text = "在系统生命周期中，被引用频次越高的页面，越是核心热点元数据或高频索引；置换时应淘汰全局累计访问频次最低的页面。"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_after = Pt(12)

    p3 = tf4_1.add_paragraph()
    p3.text = "初学者常见实现陷阱：最小堆 (Min-Heap)"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_RED
    p3.space_after = Pt(4)

    heap_trap = [
      "若使用优先队列/最小堆维护频次，每次命中频次自增后，需执行 Heap-SiftDown/Up 调整，时间复杂度退化至 O(log N)！",
      "在海量缓冲池（如 100GB 内存包含数千万页面）中，O(log N) 的额外开销完全无法承受，必须寻求严格 O(1) 解法。"
    ]
    for b in heap_trap:
        p = tf4_1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "突破极限：Ketan Shah et al. O(1) LFU 结构", COLOR_GREEN)
    box4_2 = s4.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf4_2 = box4_2.text_frame
    tf4_2.word_wrap = True

    p = tf4_2.paragraphs[0]
    p.text = "双哈希表 + 频次桶双链表结构"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(8)

    diag_lfu = (
      "min_freq 指针 ──► [ Freq = 1 桶 ] ◄──► [ Freq = 2 桶 ] ◄──► [ Freq = 5 桶 ]\n"
      "                        │                    │                     │\n"
      "                   ┌────┴────┐          ┌────┴────┐           ┌────┴────┐\n"
      "                   │ P1 ◄─► P3│          │   P2    │           │ P4 (Hot)│\n"
      "                   └─────────┘          └─────────┘           └─────────┘\n"
      "                   (Tie-Break)          (升级进新桶)          (长期热点)"
    )
    p_diag = tf4_2.add_paragraph()
    p_diag.text = diag_lfu
    p_diag.font.size = Pt(9.5)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_GREEN
    p_diag.space_after = Pt(10)

    lfu_steps = [
      ("命中升级 (Hit)", "节点从 Freq=K 桶移出，加入 Freq=K+1 桶。若原桶为空且原频次等于 min_freq，则 min_freq++。耗时严格 O(1)！"),
      ("未命中淘汰 (Evict)", "直接从 min_freq 对应的最低频次桶中弹出最老节点（Tie-Break 决胜），耗时严格 O(1)！"),
      ("新页载入", "插入 Freq=1 的桶头部，将 min_freq 重置为 1。")
    ]
    for s_t, s_d in lfu_steps:
        p = tf4_2.add_paragraph()
        p.text = f"• {s_t}：{s_d}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(4)

    s4.notes_slide.notes_text_frame.text = "很多人误以为 LFU 必须用最小堆实现，导致 O(log N) 的复杂度。其实工业界标准算法是通过频次桶双向链表，加上 min_freq 指针，将命中升级与尾部淘汰完全做到了 O(1)。"

    # ==========================================
    # SLIDE 5: 正常过程与状态流转对比
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "04. 正常过程对比：同构访问序列下的状态机分流演练")

    # 对比表格
    table_shape = s5.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(3.4)
    table.columns[3].width = Inches(3.533)

    headers = ["执行阶段", "操作序列与事件", "LRU (最近最少使用) 响应", "LFU (最不经常使用) 响应"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_BLUE if col_idx != 3 else COLOR_GREEN

    rows_data = [
      ("阶段 1：冷启动填充", "依次访问: P1, P2, P3, P4\n(容量 Capacity = 4)", "Frame 0~3 依次填入，双向链表维持: P4 -> P3 -> P2 -> P1。发生 4 次 MISS。", "Frame 0~3 依次填入，所有页面均挂在 Freq=1 桶中，min_freq=1。发生 4 次 MISS。"),
      ("阶段 2：常规热点命中", "再次访问: P1, P2\n(已有页面重复读取)", "P1, P2 命中！依次移至链表 MRU 头部，当前序: P2 -> P1 -> P4 -> P3。命中率 33%。", "P1, P2 命中！频次增至 2，晋升至 Freq=2 桶。min_freq 维持 1。命中率 33%。"),
      ("阶段 3：首度满载淘汰", "新访问页面: P5\n(未命中且缓冲池已满)", "判定 LRU 尾部为 P3，淘汰 P3，P5 插入 MRU 头。新序: P5 -> P2 -> P1 -> P4。", "min_freq=1 桶中有 P4 与 P3，按 FIFO 淘汰先入桶的 P3。P5 进 Freq=1 桶。"),
      ("阶段 4：局部性验证", "再次访问: P1, P2\n(持续热点访问)", "P1, P2 再次命中，刷新至 MRU。置换结果表现优异。", "P1, P2 再次命中，频次累加至 3，筑牢热点频次壁垒。"),
      ("机制特性小结", "基于时间衰减", "对时间极为敏感，最近访问的页面永远有最高生存优先级。", "对频次极其崇拜，只要历史上累计频次高，就能免疫淘汰。")
    ]

    for r_idx, r in enumerate(rows_data):
        for c_idx, val in enumerate(r):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(20, 29, 47) if r_idx % 2 == 0 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT

    # 底部说明卡片
    sum_card = add_card(s5, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.8))
    s_box = s5.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.7))
    s_tf = s_box.text_frame
    s_p = s_tf.paragraphs[0]
    s_p.text = "【核心结论】在常规倾斜访问（Skewed Zipfian Distribution）且无工作集剧烈波动的场景下，LRU 与 LFU 均能取得 70%~90% 的优异命中率，两者行为在稳态下高度趋同。"
    s_p.font.size = Pt(11)
    s_p.font.bold = True
    s_p.font.color.rgb = COLOR_AMBER

    s5.notes_slide.notes_text_frame.text = "在正常访问流程下，两算法均表现出良好的局部性适应能力。LRU 不断将命中页面推至 MRU 头部，LFU 则将命中页面提升至更高的频次桶。稳态下两者的命中率差异并不显著。"

    # ==========================================
    # SLIDE 6: 算法边界情形处理
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "05. 算法边界情形剖析：冷启动、同频争用 (Tie-Breaking) 与突发冲击")

    # 卡片 1: 冷启动
    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "边界一：空池冷启动 (Cold Start)", COLOR_BLUE)
    b1_box = s6.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.2), Inches(4.4))
    b1_tf = b1_box.text_frame
    b1_tf.word_wrap = True

    b1_items = [
      ("物理内存初始状态", "数据库刚启动时，Buffer Pool 所有 Frame 均处于未分配状态（Free List 维护可用空槽）。"),
      ("两算法一致性表现", "在 Free List 消耗殆尽之前，LRU 和 LFU 均无需触发淘汰逻辑，每次缺页直接分配空闲 Frame，属于机械冷填充。"),
      ("工程预热 (Warm-up)", "生产环境必须防止冷启动直接接入高峰流量。现代数据库支持重启时自动从预热文件恢复 Buffer Pool 内存页映射。")
    ]
    for idx, (t, d) in enumerate(b1_items):
        p = b1_tf.paragraphs[0] if idx == 0 else b1_tf.add_paragraph()
        p.text = f"• {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = b1_tf.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(8)

    # 卡片 2: Tie-Breaking
    add_card(s6, Inches(4.7), Inches(1.6), Inches(4.2), Inches(5.2), "边界二：同频竞争仲裁 (Tie-Breaking)", COLOR_AMBER)
    b2_box = s6.shapes.add_textbox(Inches(4.9), Inches(2.2), Inches(3.8), Inches(4.4))
    b2_tf = b2_box.text_frame
    b2_tf.word_wrap = True

    b2_items = [
      ("冲突核心痛点", "当缓冲池已满，且最低频次桶 (min_freq) 内同时存在多个页面（例如页面 A、B、C 频次均为 1），LFU 该淘汰谁？"),
      ("裁决法则 (Tie-breaker)", "必须引入次级决胜规则！标准解法为：在同一频次桶内使用双向链表维护先后顺序（FIFO 或 LRU 规则）。"),
      ("确定性淘汰保证", "优先驱逐最早进入该频次桶的尾部节点，保证算法行为严格确定且可预测，避免震荡。")
    ]
    for idx, (t, d) in enumerate(b2_items):
        p = b2_tf.paragraphs[0] if idx == 0 else b2_tf.add_paragraph()
        p.text = f"★ {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_AMBER
        pd = b2_tf.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(8)

    # 卡片 3: 突发重复脉冲
    add_card(s6, Inches(9.2), Inches(1.6), Inches(3.3), Inches(5.2), "边界三：突发脉冲与频繁反转", COLOR_PURPLE)
    b3_box = s6.shapes.add_textbox(Inches(9.4), Inches(2.2), Inches(2.9), Inches(4.4))
    b3_tf = b3_box.text_frame
    b3_tf.word_wrap = True

    b3_items = [
      ("循环交替扫描", "当工作集大小恰好为 Capacity + 1 时，循环访问将导致 LRU 命中率直降为 0%！"),
      ("突发高频暴击", "某个临时数据页在极短时间内被集中读取数十次，导致频次瞬间飞涨，破坏全局频次分布的均衡性。"),
      ("边界启示", "极端访问模式会放大单一启发式指标的固有偏见。")
    ]
    for idx, (t, d) in enumerate(b3_items):
        p = b3_tf.paragraphs[0] if idx == 0 else b3_tf.add_paragraph()
        p.text = f"▲ {t}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PURPLE
        pd = b3_tf.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(8)

    s6.notes_slide.notes_text_frame.text = "边界场景是检验算法鲁棒性的试金石。特别是在 LFU 中，当多个页面频次相同时，必须依靠严格的 Tie-breaking 决胜规则淘汰桶内最老页面，才能维持 O(1) 的确定性。"

    # ==========================================
    # SLIDE 7: 异常反例 1 - LRU 全表扫描污染
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "06. 异常与反例 ①：全表扫描引发的 LRU 缓存污染 (Cache Pollution)")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "灾难场景：全表扫描冲刷 (Sequential Scan)", COLOR_RED)
    s7_1 = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf7_1 = s7_1.text_frame
    tf7_1.word_wrap = True

    p = tf7_1.paragraphs[0]
    p.text = "生产环境典型事故复现"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_after = Pt(6)

    pollution_story = [
      ("稳态热点运行", "Buffer Pool 原本缓存了核心用户表、订单主键索引根节点（Hot_1, Hot_2, Hot_3），高频命中。"),
      ("慢查询突发介入", "业务执行无索引扫描查询：SELECT * FROM Big_Log WHERE date = '...'，涉及数万张一次性冷页面（S_1, S_2, S_3...）。"),
      ("LRU 的致命盲区", "LRU 只看‘最近访问时间’。新涌入的冷数据被误认作‘最重要的数据’，源源不断插入 MRU 头部！"),
      ("全军覆没的结果", "真正的事务热点页面被无情推向链表尾部并逐一驱逐！扫描结束后，后续 OLTP 交易全部发生磁盘缺页，系统吞吐量断崖式暴跌（缓存穿透与击穿）！")
    ]
    for h, b in pollution_story:
        p = tf7_1.add_paragraph()
        p.text = f"• {h}："
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf7_1.add_paragraph()
        pd.text = b
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(6)

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "同等冲击下的 LFU 优异防御表现", COLOR_GREEN)
    s7_2 = s7.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf7_2 = s7_2.text_frame
    tf7_2.word_wrap = True

    p = tf7_2.paragraphs[0]
    p.text = "LFU 的天然频次免疫防线"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(8)

    diag_seq = (
      "[ 全表扫描冷数据流入: S1 -> S2 -> S3 -> S4 ... ]\n"
      "   S_i 页面仅读取 1 次，其频次永远为: Freq = 1\n\n"
      "[ LFU 缓冲池内存状态 ]\n"
      "   ┌──────────────────────────────────────────────┐\n"
      "   │ 频次壁垒防护区 (Freq >= 5):                  │\n"
      "   │   Hot_Index_1, Hot_User_2 (绝对免死，安然无恙)│\n"
      "   ├──────────────────────────────────────────────┤\n"
      "   │ 最低频次置换区 (min_freq = 1):               │\n"
      "   │   S_1 进入 -> S_2 替换 S_1 -> S_3 替换 S_2... │\n"
      "   └──────────────────────────────────────────────┘\n"
      "   (冷数据仅在 1 个物理槽内自我踩踏，绝不污染核心热点！)"
    )
    p_diag = tf7_2.add_paragraph()
    p_diag.text = diag_seq
    p_diag.font.size = Pt(9.5)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_GREEN
    p_diag.space_after = Pt(12)

    p_conc = tf7_2.add_paragraph()
    p_conc.text = "【反例评分结论】在面对大规模一次性全表扫描时，LFU 展现出远胜于原生 LRU 的防御力，历史频次壁垒有效隔离了单次批处理冲击。"
    p_conc.font.size = Pt(11)
    p_conc.font.bold = True
    p_conc.font.color.rgb = COLOR_AMBER

    s7.notes_slide.notes_text_frame.text = "这是第一个最具杀伤力的反例：全表扫描缓存污染。在 LRU 中，一次全表扫描就把所有宝贵热点刷出内存；而 LFU 中，由于扫描页频次仅为 1，它只会在 min_freq 桶内自我置换，核心热点毫发无损！"

    # ==========================================
    # SLIDE 8: 异常反例 2 - LFU 历史频次僵死
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "07. 异常与反例 ②：历史频次积累引发的 LFU 缓存僵死 (Cache Sclerosis)")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "灾难场景：工作集漂移与僵尸缓存", COLOR_RED)
    s8_1 = s8.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf8_1 = s8_1.text_frame
    tf8_1.word_wrap = True

    p = tf8_1.paragraphs[0]
    p.text = "LFU 频次崇拜的致命病态退化"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_after = Pt(6)

    sclerosis_story = [
      ("早期突发爆发", "某页面 Ghost 在系统初始化或特定大促秒杀活动中，短时间内被访问了 1000 次，其频次高达 Freq = 1000。"),
      ("工作集彻底漂移 (Phase Shift)", "活动结束，业务模式切换至新模块，Ghost 页面未来再也不会被访问一次。"),
      ("僵死与锁死 (Sclerosis)", "由于缺少时间衰减机制，Ghost 凭借 1000 的高频护身符，永久霸占缓冲槽位（成为‘僵尸页面’）。"),
      ("新工作集饥饿饿死 (Starvation)", "新模块产生的新活跃页面（N_1, N_2...）初入频次均为 1，在有限的残存槽位中疯狂相互践踏，LFU 命中率暴跌趋近于 0%！")
    ]
    for h, b in sclerosis_story:
        p = tf8_1.add_paragraph()
        p.text = f"• {h}："
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf8_1.add_paragraph()
        pd.text = b
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(6)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "LRU 面对工作集漂移的天然敏捷自适应", COLOR_BLUE)
    s8_2 = s8.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf8_2 = s8_2.text_frame
    tf8_2.word_wrap = True

    p = tf8_2.paragraphs[0]
    p.text = "时间局部性的自我修正优势"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(8)

    diag_shift = (
      "[ 工作集漂移事件发生: 放弃 Ghost，全面访问 N1, N2, N3 ... ]\n\n"
      "[ LRU 链表自适应过程 ]\n"
      "   1. N1, N2, N3 进入，插入 MRU 头部；\n"
      "   2. 随着时间推移，没有任何新访问的 Ghost 自然滑向尾部；\n"
      "   3. 经过 Capacity 次替换后，Ghost 被平滑驱逐出池；\n"
      "   4. 缓冲池无缝收敛至新工作集，命中率迅速回升至 90%+！\n\n"
      "【本质哲学对比】\n"
      "• LRU: 遗忘历史，面向未来（高动态适应性，但怕扫描）；\n"
      "• LFU: 沉湎历史，墨守成规（抗扫描，但怕漂移与僵死）。"
    )
    p_diag = tf8_2.add_paragraph()
    p_diag.text = diag_shift
    p_diag.font.size = Pt(9.5)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_BLUE
    p_diag.space_after = Pt(10)

    p_conc2 = tf8_2.add_paragraph()
    p_conc2.text = "【反例破局关键】工业级 LFU 必须引入频次老化（Aging / Decay）或时间滑动窗口衰减，否则根本无法在长周期运行的数据库中落地。"
    p_conc2.font.size = Pt(11)
    p_conc2.font.bold = True
    p_conc2.font.color.rgb = COLOR_AMBER

    s8.notes_slide.notes_text_frame.text = "反过来，这就是 LFU 最致命的死穴：历史频次僵死。早期爆发的高频幽灵数据永远赖在内存里，导致新工作集被饥饿淘汰。此时 LRU 的时间遗忘机制反而展现出强大的敏捷自适应优势。"

    # ==========================================
    # SLIDE 9: 交互动画演示系统架构
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "08. 成果展示：自研双引擎交互式动画演示系统设计")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "动画系统技术架构与全功能设计", COLOR_BLUE)
    s9_1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf9_1 = s9_1.text_frame
    tf9_1.word_wrap = True

    features = [
      ("原生零依赖渲染 (Pure Vanilla HTML5/SVG/CSS3)", "跨平台单文件即可独立运行，无外部 CDN 依赖，彻底规避断网答辩风险。"),
      ("双置换引擎同屏毫秒级联动", "左侧 LRU 双向链表 vs 右侧 LFU O(1) 频次桶，单步推进完全同构驱动，实时对比每一帧的指针变迁。"),
      ("声画同步智能旁白引擎 (Web Speech API)", "内置语音合成与动态字幕，精确指示“命中提升”、“缺页载入”、“同频仲裁”与“反例爆发”。"),
      ("五大预设场景与自定义压测流水线", "涵盖 5分钟剧本演示、常规流水、边界仲裁、全表扫描冲刷、频次僵死，并支持任意输入页面流实时评测。")
    ]
    for h, d in features:
        p = tf9_1.add_paragraph()
        p.text = f"★ {h}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf9_1.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(6)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "动画界面核心视图布局分布", COLOR_GREEN)
    s9_2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf9_2 = s9_2.text_frame
    tf9_2.word_wrap = True

    ui_layout = (
      "┌────────────────────────────────────────────────────────┐\n"
      "│ 顶部控制台: 场景选择(5分钟/反例) | 播放控制 | 倍速 | 容量 │\n"
      "├────────────────────────────────────────────────────────┤\n"
      "│ 讲解员横幅: 阶段状态 | 时间轴(00:00~05:00) | 实时解说字幕│\n"
      "├────────────────────────────────────────────────────────┤\n"
      "│ 请求流水线: [P1] -> [P2] -> [P3] -> [P4] (高亮当前REQ)  │\n"
      "├──────────────────────────┬─────────────────────────────┤\n"
      "│ 【左翼: LRU 引擎】        │ 【右翼: LFU 引擎】           │\n"
      "│ • 物理缓冲帧 (Pin/Dirty) │ • 物理缓冲帧 (Freq 标定)    │\n"
      "│ • MRU ◄──► LRU 双向链表   │ • O(1) 频次桶 + min_freq    │\n"
      "│ • 实时命中率与驱逐统计   │ • 实时命中率与驱逐统计      │\n"
      "├──────────────────────────┴─────────────────────────────┤\n"
      "│ 底部看板: 累积命中率柱状图 | 学术内核机制启示总结      │\n"
      "└────────────────────────────────────────────────────────┘"
    )
    p_ui = tf9_2.add_paragraph()
    p_ui.text = ui_layout
    p_ui.font.size = Pt(8.5)
    p_ui.font.name = "Courier New"
    p_ui.font.color.rgb = COLOR_BLUE
    p_ui.space_after = Pt(10)

    p_run = tf9_2.add_paragraph()
    p_run.text = "交付文件：`演示文稿/index.html`，双击或以任意现代浏览器打开即可享受 60FPS 丝滑交互动画体验！"
    p_run.font.size = Pt(11)
    p_run.font.bold = True
    p_run.font.color.rgb = COLOR_GREEN

    s9.notes_slide.notes_text_frame.text = "为了让评委老师直观看到算法细节，我们自主研发了基于 HTML5 的双引擎同屏动画系统。该系统不仅支持单步调试，还内建了 5 分钟自动演讲剧本和声画同步旁白。"

    # ==========================================
    # SLIDE 10: 5分钟现场演示实况时间轴
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "09. 5分钟现场演示实况脚本与时间轴精准对齐")

    t_box = s10.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.5))
    tf10 = t_box.text_frame
    tf10.word_wrap = True

    timeline_items = [
      ("00:00 - 00:50 (50s)", "阶段一：缓冲池机制与冷启动加载", "连续访问 P1~P4。演示内存帧分配、Page Table 哈希表建立、Free List 耗尽，两算法处于冷填充稳态。", "向老师展示基础数据结构初始化与物理帧映射。"),
      ("00:50 - 01:45 (55s)", "阶段二：常规命中与数据结构状态迁移", "重复读取 P1、P2 并引入 P5。演示 LRU 节点指针移动至 MRU 头部；LFU 节点跨桶升级至 Freq=2 并触发首度置换。", "强调 LRU 与 LFU 在时间 vs 频次两种假设下的分水岭。"),
      ("01:45 - 02:45 (60s)", "阶段三：边界情形与同频仲裁 (Tie-Breaking)", "触发同为 Freq=1 的页面竞争。展示 LFU 如何依据桶内链表 FIFO/LRU 次级规则精确淘汰最老进入者，消除震荡。", "证明 LFU 实现了确定性与严格常数级 O(1) 仲裁。"),
      ("02:45 - 03:45 (60s)", "阶段四：异常反例大对决 ① —— 全表扫描冲击", "模拟一次性扫描流 S1~S5 疯狂冲刷。直观呈现 LRU 命中率惨烈暴跌至 0%，而 LFU 依靠频次壁垒完美守住热点。", "现场最震撼反例展示，揭露原生 LRU 工业落地的致命痛点。"),
      ("03:45 - 04:30 (45s)", "阶段五：异常反例大对决 ② —— 频次僵死与漂移", "构造高频历史幽灵页 G_Old 与全新工作集 N1~N4。展示 LFU 僵死沦陷与新页饿死，而 LRU 敏捷自我修复。", "反转高潮！证明没有绝对完美的算法，只有对场景的妥协。"),
      ("04:30 - 05:00 (30s)", "阶段六：工业界破局演化与答辩总结", "引入 PostgreSQL Clock-Sweep 与 MySQL InnoDB Midpoint 真实代码级实现，引出答辩 Q&A。", "升华主题，完成从教科书理论到工业级数据库内核的跨越。")
    ]

    for idx, (time_span, stage_title, action_desc, teach_note) in enumerate(timeline_items):
        card_t = add_card(s10, Inches(0.8), Inches(1.55 + idx * 0.9), Inches(11.733), Inches(0.82))
        c_box = s10.shapes.add_textbox(Inches(0.9), Inches(1.57 + idx * 0.9), Inches(11.5), Inches(0.78))
        c_tf = c_box.text_frame
        c_tf.word_wrap = True

        p = c_tf.paragraphs[0]
        p.text = f"【{time_span}】 {stage_title}"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE if idx < 3 else (COLOR_RED if idx in [3, 4] else COLOR_GREEN)

        p2 = c_tf.add_paragraph()
        p2.text = f"演示动作: {action_desc}  |  讲解要点: {teach_note}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_MUTED

    s10.notes_slide.notes_text_frame.text = "这是我们 5 分钟动画演示的严密时间轴。每一阶段精确到秒，从冷启动、常规命中、边界仲裁，层层递进到两大致命反例，最后引申至工业界破局，节奏紧凑有力。"

    # ==========================================
    # SLIDE 11: 现代工业演化 1 - PostgreSQL Clock
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10. 现代工业级破局演化 ①：PostgreSQL 的 Clock-Sweep 时钟置换")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "PostgreSQL 内核痛点与时钟机制", COLOR_BLUE)
    s11_1 = s11.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf11_1 = s11_1.text_frame
    tf11_1.word_wrap = True

    p = tf11_1.paragraphs[0]
    p.text = "为什么 PostgreSQL 放弃纯 LRU 双链表？"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    pg_reasons = [
      ("并发锁瓶颈 (Lock Contention)", "纯 LRU 每次命中都必须加互斥锁修改全局双链表指针。高并发读场景下，锁竞争将吞噬全部 CPU 算力！"),
      ("时钟置换 (Clock Sweep) 方案", "将全部物理缓冲帧组织为环形数组，维护全局指针 nextVictimBuffer 单向旋转。"),
      ("usage_count 引用计数器 (0~5)", "每个 Buffer Descriptor 维护一个原子整型 usage_count，初始为 1，命中时原子自增（最大上限 5，防止无限膨胀）。"),
      ("极低锁开销无锁设计", "读取命中无需修改链表指针，仅执行一条原子自增指令；置换时才推进时钟指针，极大提升多核伸缩性。")
    ]
    for h, d in pg_reasons:
        p = tf11_1.add_paragraph()
        p.text = f"• {h}："
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf11_1.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(6)

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Clock-Sweep 置换扫描流程与源码对照", COLOR_GREEN)
    s11_2 = s11.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf11_2 = s11_2.text_frame
    tf11_2.word_wrap = True

    p = tf11_2.paragraphs[0]
    p.text = "PostgreSQL freelist.c 核心扫描逻辑图解"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(8)

    diag_clock = (
      "        [ Frame 0: usage_count=2 ]\n"
      "      ↗                            ↖\n"
      "[ Frame 3: usage=0 ] ◄── 指针 ──► [ Frame 1: usage=1 ]\n"
      "      (驱逐目标!)                  (指针扫过自减为 0)\n"
      "      ↘                            ↙\n"
      "        [ Frame 2: Pin > 0 (跳过) ]\n\n"
      "【时钟指针扫描步骤】\n"
      "1. 检查当前缓冲帧 Pin Count，若 Pin > 0 则跳过；\n"
      "2. 若 usage_count > 0，则 usage_count 自减 1，指针前移；\n"
      "3. 直到找到首个 usage_count == 0 且 Pin == 0 的槽位，执行驱逐！"
    )
    p_diag = tf11_2.add_paragraph()
    p_diag.text = diag_clock
    p_diag.font.size = Pt(9.5)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_BLUE
    p_diag.space_after = Pt(10)

    p_eval = tf11_2.add_paragraph()
    p_eval.text = "【机制精妙点】指针每完整旋转一圈，所有页面的 usage_count 均自然衰减 1。这实际上在常数开销下优雅融合了 LFU 的频次累积与 LRU 的时间衰减！"
    p_eval.font.size = Pt(11)
    p_eval.font.bold = True
    p_eval.font.color.rgb = COLOR_AMBER

    s11.notes_slide.notes_text_frame.text = "PostgreSQL 之所以不采用纯 LRU，是为了解决多核高并发下的锁争用。Clock-Sweep 算法用一个环形时钟指针和 0~5 的 usage_count，既实现了频次统计，又在旋转中实现了时间衰减，且读命中无需拿大锁。"

    # ==========================================
    # SLIDE 12: 现代工业演化 2 - MySQL InnoDB Midpoint LRU
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11. 现代工业级破局演化 ②：MySQL InnoDB 的 Midpoint Insertion LRU")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "InnoDB 分代 LRU 体系结构", COLOR_BLUE)
    s12_1 = s12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf12_1 = s12_1.text_frame
    tf12_1.word_wrap = True

    p = tf12_1.paragraphs[0]
    p.text = "双段子链表架构 (5/8 与 3/8 分割)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    innodb_concepts = [
      ("打破传统头部插入", "传统 LRU 新数据入 MRU 头部。InnoDB 将 LRU 链表划分为两截：New Sublist (Young 区，默认 5/8) 与 Old Sublist (冷区，默认 3/8)。"),
      ("Midpoint 中点插入法", "磁盘载入的新页面绝不直接进入 Young 头部，而是插入 Old 区头部（即链表的 5/8 中点位置）！"),
      ("两道防线有效隔离", "由于新页面只能在 Old 区活动，无论全表扫描读入多少数据，扫描冲击全部被死死封锁在 3/8 的 Old 区内，Young 区的核心热点毫发无损！")
    ]
    for h, d in innodb_concepts:
        p = tf12_1.add_paragraph()
        p.text = f"• {h}："
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf12_1.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(6)

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "时间窗口过滤参数：innodb_old_blocks_time", COLOR_AMBER)
    s12_2 = s12.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf12_2 = s12_2.text_frame
    tf12_2.word_wrap = True

    p = tf12_2.paragraphs[0]
    p.text = "InnoDB 抑制全表扫描的关键机制"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(8)

    diag_innodb = (
      "[ MRU Head ] ────────── Young Sublist (5/8) ──────────► [ Midpoint ]\n"
      "   ▲ (真正的核心长期热数据)                                  │\n"
      "   │ 停留超过 1000ms 且再被访问才晋升                        │ (新页插入点)\n"
      "   └──────────────────────────┐                              ▼\n"
      "   [ Midpoint ] ────────── Old Sublist (3/8) ──────────► [ LRU Tail ]\n"
      "      (全表扫描冷数据在此区快速淘汰，绝无机会侵入 Young 区)"
    )
    p_diag = tf12_2.add_paragraph()
    p_diag.text = diag_innodb
    p_diag.font.size = Pt(9)
    p_diag.font.name = "Courier New"
    p_diag.font.color.rgb = COLOR_AMBER
    p_diag.space_after = Pt(10)

    params = [
      ("innodb_old_blocks_pct", "控制 Old 区所占百分比（默认 37% 即 3/8）。"),
      ("innodb_old_blocks_time", "晋升冷却时间窗口（默认 1000 ms）。全表扫描的一页在 1秒内可能被多次迭代读取，但因在 1000ms 内，绝不晋升！扫描结束即随尾部淘汰，彻底破解 LRU 缓存污染！")
    ]
    for p_n, p_d in params:
        p = tf12_2.add_paragraph()
        p.text = f"★ 参数 `{p_n}`："
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT
        pd = tf12_2.add_paragraph()
        pd.text = p_d
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_MUTED
        pd.space_after = Pt(4)

    s12.notes_slide.notes_text_frame.text = "针对前面提到的 LRU 全表扫描污染，MySQL InnoDB 给出了教科书级的工业解法：Midpoint 5/8 插入法加 innodb_old_blocks_time 1000ms 冷却时间。扫描的页面哪怕读 100 次，只要在 1 秒内，都无法进入 Young 区！"

    # ==========================================
    # SLIDE 13: 前沿混合演进：LRU-K, 2Q, W-TinyLFU
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "12. 前沿学术与现代缓存演化：LRU-K、2Q 与 W-TinyLFU")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2), "LRU-K 算法 (O'Neil et al.)", COLOR_BLUE)
    c1 = s13.shapes.add_textbox(Inches(0.95), Inches(2.2), Inches(3.3), Inches(4.4))
    tf1 = c1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "后退 K 次访问时间倒排"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    bullets_k = [
      "传统 LRU 相当于 LRU-1，极易受突发单次扫描欺骗。",
      "LRU-K 跟踪每个页面最近 K 次访问的历史时间戳。驱逐时，比较距今‘倒数第 K 次引用的时间距离’（Backward K-distance）。",
      "访问不足 K 次的页面被赋予无穷大距离优先驱逐。",
      "工业界通常取 K=2 (LRU-2)，即可近乎完美地过滤一切单次扫描污染。"
    ]
    for b in bullets_k:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    add_card(s13, Inches(4.7), Inches(1.6), Inches(4.2), Inches(5.2), "2Q 算法 (Johnson & Shasha)", COLOR_GREEN)
    c2 = s13.shapes.add_textbox(Inches(4.85), Inches(2.2), Inches(3.9), Inches(4.4))
    tf2 = c2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "双队列与常数级 O(1) 简易滤波"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    bullets_2q = [
      "为了避免 LRU-2 维护优先队列的时间开销，2Q 引入了两个简单队列：A1 in (FIFO) 与 Am (LRU)。",
      "新载入页面首先进入 A1 in 队列；如果页面在 A1 in 中被淘汰出内存，仅保留其 key 在 A1 out 描述符中。",
      "若页面在 A1 out 期间再次被引用，则将其正式晋升并迁入永久热点队列 Am (LRU)。",
      "以 O(1) 复杂度实现了与 LRU-2 相当的抗污染特性。"
    ]
    for b in bullets_2q:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    add_card(s13, Inches(9.2), Inches(1.6), Inches(3.3), Inches(5.2), "W-TinyLFU (现代缓存王者)", COLOR_PURPLE)
    c3 = s13.shapes.add_textbox(Inches(9.35), Inches(2.2), Inches(3.0), Inches(4.4))
    tf3 = c3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "Caffeine / 现代内存中间件标配"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT
    p.space_after = Pt(6)

    bullets_w = [
      "采用 Window LRU (1% 缓冲区容量) 接纳新流量，防止新突发页面被误杀。",
      "主缓存划分为 Probation (试用区) 与 Protected (保护区)。",
      "引入 Count-Min Sketch 4-bit 紧凑哈希统计频次，空间极小。",
      "重置老化机制：当样本计数达到门限时，全表计数值右移除以2，彻底铲除 LFU 历史频次僵死！"
    ]
    for b in bullets_w:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)

    s13.notes_slide.notes_text_frame.text = "在学术界与高性能缓存框架中，LRU-K、2Q 和 W-TinyLFU 代表了现代置换策略的最高峰。特别是 W-TinyLFU，通过 Count-Min Sketch 和减半老化机制，彻底解决了 LFU 频次僵死的问题。"

    # ==========================================
    # SLIDE 14: 综合评估矩阵与选型指南
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "13. 综合性能评估矩阵与工程选型决策树")

    # 对比综合大表格
    table_shape14 = s14.shapes.add_table(6, 6, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5))
    tbl14 = table_shape14.table
    tbl14.columns[0].width = Inches(2.1)
    tbl14.columns[1].width = Inches(1.9)
    tbl14.columns[2].width = Inches(1.9)
    tbl14.columns[3].width = Inches(1.9)
    tbl14.columns[4].width = Inches(1.9)
    tbl14.columns[5].width = Inches(2.033)

    cols14 = ["算法名称", "命中时间复杂度", "空间开销", "抗全表扫描", "抗频次僵死", "工业代表实现"]
    for c_i, h in enumerate(cols14):
        cell = tbl14.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_BLUE

    matrix_data = [
      ("原生 LRU", "O(1) [需全局锁]", "中 (双向指针)", "差 (极易被击穿)", "极优 (自然遗忘)", "传统小型引擎/教学示范"),
      ("原生 O(1) LFU", "O(1) [双链桶]", "较高 (桶链+节点)", "优 (频次壁垒隔离)", "差 (无衰减则僵死)", "极少直接使用"),
      ("PostgreSQL Clock", "O(1) [无链表锁]", "极低 (1个原子整型)", "中等 (受限衰减)", "良好 (指针旋转衰减)", "PostgreSQL, SQLite"),
      ("InnoDB Midpoint LRU", "O(1) [分段链表]", "中 (双指针+时间戳)", "极优 (1000ms 隔离)", "优 (Young/Old分代)", "MySQL InnoDB 存储引擎"),
      ("W-TinyLFU", "O(1) [平摊常数]", "极低 (TinySketch)", "极优 (Window缓冲)", "极优 (Halving 衰减)", "Caffeine, 高性能内存池")
    ]
    for r_i, row in enumerate(matrix_data):
        for c_i, val in enumerate(row):
            cell = tbl14.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(20, 29, 47) if r_i % 2 == 0 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT

    # 选型指导卡片
    g_card = add_card(s14, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.8))
    g_box = s14.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.7))
    g_tf = g_box.text_frame
    g_p = g_tf.paragraphs[0]
    g_p.text = "【数据库架构选型法则】纯粹的算法在真实生产环境必然遭遇病态退化。生产系统优先选用‘低锁竞争 + 空间分代 + 频次衰减’的复合架构（如 PG Clock 与 InnoDB Midpoint）。"
    g_p.font.size = Pt(11)
    g_p.font.bold = True
    g_p.font.color.rgb = COLOR_GREEN

    s14.notes_slide.notes_text_frame.text = "通过横向矩阵对比，我们清晰地看到没有绝对的银弹。工业界之所以青睐 Clock 和 Midpoint LRU，是因为它们在极低锁开销和抗异常冲刷之间找到了完美的平衡点。"

    # ==========================================
    # SLIDE 15: 组员分工与团队协作
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "14. 实验组织、组员分工矩阵与 AI 协同研发创新")

    # 3人分工卡片
    roles = [
      ("组长 (Leader)", "贡献度: 35%", COLOR_BLUE, [
        "负责置换机制理论推演与严密形式化建模；",
        "剖析并构造全表扫描污染与历史频次僵死两大极端反例；",
        "统筹撰写 5分钟现场逐字演说稿与答辩核心预案；",
        "把控交付物质量，确保符合 99+ 评审标准。"
      ]),
      ("组员一 (内核与动画研发)", "贡献度: 33%", COLOR_GREEN, [
        "主导自研 HTML5/Canvas/CSS3 交互仿真动画系统；",
        "独立编码实现 LRU O(1) 双链表与 LFU O(1) 频次桶算法；",
        "开发 Web Speech 语音旁白引擎与 5分钟自动化剧本；",
        "负责动画性能调优，实现 60FPS 丝滑高保真渲染。"
      ]),
      ("组员二 (工业演化与答辩)", "贡献度: 32%", COLOR_PURPLE, [
        "深度研读 PostgreSQL (bufmgr.c) 与 MySQL (buf0lru.cc) 源码；",
        "提炼 Clock-Sweep 与 Midpoint 插入法的工程对应；",
        "制定 20+ 道答辩刁钻提问与标准高分回答手册；",
        "协助 PPT 生成与交互系统极限用例压测验证。"
      ])
    ]

    for idx, (r_name, r_pct, r_color, r_tasks) in enumerate(roles):
        add_card(s15, Inches(0.8 + idx * 4.0), Inches(1.6), Inches(3.7), Inches(3.8), f"{r_name} · {r_pct}", r_color)
        t_box = s15.shapes.add_textbox(Inches(0.95 + idx * 4.0), Inches(2.2), Inches(3.4), Inches(3.0))
        tf = t_box.text_frame
        tf.word_wrap = True
        for t_idx, t in enumerate(r_tasks):
            p = tf.paragraphs[0] if t_idx == 0 else tf.add_paragraph()
            p.text = "• " + t
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_MUTED
            p.space_after = Pt(4)

    # 底部 AI 协同研发卡片
    ai_card = add_card(s15, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.5), "AI 工具协同研发与提示词工程 (Prompt Engineering)", COLOR_AMBER)
    ai_box = s15.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.9))
    ai_tf = ai_box.text_frame
    ai_tf.word_wrap = True
    ai_p = ai_tf.paragraphs[0]
    ai_p.text = "• 提示词链设计：采用思维链 (Chain-of-Thought) 进行 O(1) LFU 双哈希桶结构的形式化推导与反例构造。\n• 自动化测试辅助：利用 AI 自动生成 1000+ 随机页面访问流并进行两算法命中率 Monte Carlo 仿真对比。\n• 说明书记录：所有核心 Prompt、系统提示词与多轮迭代演化过程均完备收录于《AI制作提示词全纪录.md》。"
    ai_p.font.size = Pt(10.5)
    ai_p.font.color.rgb = COLOR_TEXT

    s15.notes_slide.notes_text_frame.text = "我们团队 3 人各司其职，紧密配合。在整个项目推进过程中，我们充分借助大模型进行提示词工程设计与算法边界推导，所有研发过程均严格留痕记录。"

    # ==========================================
    # SLIDE 16: 现场答辩高频核心问题预案与致谢
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "15. 答辩核心高频问题防线 (Q&A Defense) 与总结致谢")

    # 4个经典提问预案卡片
    qas = [
      ("Q1: 并发环境下纯 LRU 为什么会引发严重瓶颈？如何解决？",
       "答：LRU 读命中也必须修改双链表指针，需要全局排他锁（Latch Contention）。现代数据库采用分区锁（Partitioned LRU）、无锁时钟置换（Clock Sweep）或批处理转移（Batching Channel）缓解锁竞争。"),
      ("Q2: 脏页 (Dirty Page) 在置换时如何处理？会直接写盘吗？",
       "答：不能直接写！必须严格遵循 WAL 协议，保证对应的 Redo Log 先刷盘。此外后台有专门的 Page Cleaner 线程异步刷脏，避免置换线程直接陷入前台同步写盘泥潭。"),
      ("Q3: LFU 的频次计数器会溢出吗？高并发下如何高效统计？",
       "答：在生产系统中计数器会设置上限（如 PG 设为 5），或采用类似 Redis/Caffeine 的 Count-Min Sketch 对数衰减计数（Logarithmic Counter），既防止溢出又极度节约内存。"),
      ("Q4: MySQL 的 innodb_old_blocks_time 设为 0 会发生什么？",
       "答：若设为 0，页面一旦在 Old 区被访问第二次就立刻晋升到 Young 区头部，全表扫描的页面在遍历读取多行记录时将瞬间把热点 Young 区冲垮，彻底丧失防污染能力！")
    ]

    for idx, (q, a) in enumerate(qas):
        top_offset = Inches(1.6 + idx * 1.15)
        add_card(s16, Inches(0.8), top_offset, Inches(11.733), Inches(1.05), "", COLOR_BORDER)
        box = s16.shapes.add_textbox(Inches(1.0), top_offset + Inches(0.08), Inches(11.3), Inches(0.9))
        tf = box.text_frame
        tf.word_wrap = True

        pq = tf.paragraphs[0]
        pq.text = q
        pq.font.size = Pt(11)
        pq.font.bold = True
        pq.font.color.rgb = COLOR_AMBER

        pa = tf.add_paragraph()
        pa.text = a
        pa.font.size = Pt(9.5)
        pa.font.color.rgb = COLOR_MUTED
        pa.space_before = Pt(3)

    # 底部致谢横幅
    t_box = s16.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.6))
    t_tf = t_box.text_frame
    t_p = t_tf.paragraphs[0]
    t_p.text = "汇报完毕，恳请各位评委老师批评指正！  |  完整动画与文档系统已就绪，欢迎进入实操体验"
    t_p.font.size = Pt(13)
    t_p.font.bold = True
    t_p.alignment = PP_ALIGN.CENTER
    t_p.font.color.rgb = COLOR_BLUE

    s16.notes_slide.notes_text_frame.text = "以上就是我们小组的全部汇报内容。我们已经准备好接受各位老师的深入提问，也欢迎老师亲自体验我们的交互动画系统。谢谢大家！"

    # 保存
    save_path = r"d:\workspace\高级数据库\动画制作\演示文稿\lru_lfu_comparison.pptx"
    prs.save(save_path)
    print(f"PowerPoint successfully created at: {save_path}")

if __name__ == "__main__":
    create_presentation()
