from kivy.lang import Builder
Builder.load_string('''
<AttributeEditor>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "right"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "30dp", "30dp"
            source: "images/ln.png"

    MDLabel:
        text: root.alias
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: root.identity_pubkey
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    MDTextField:
        text: '{:_}'.format(root.channel.earned if root.channel else 0)
        helper_text: 'Earned'
        helper_text_mode: 'persistent'

    ScrollView:
        DrawerList:
            id: md_list

''')
Builder.load_string('''
########################################################################################
# INGEST INVOICES
########################################################################################

<IngestInvoicesScreen>:
    size_hint: .8, .8
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    count: count
    title: 'Ingest Invoices'
    BoxLayout:
        padding: 20
        spacing: 20
        orientation: 'vertical'
        GridLayout:
            cols: 1
            padding: 20
            spacing: 20
            BoxLayout:
                size_hint_y: None
                height: 150
                orientation: 'horizontal'
                Label:
                    text: "Ingest"
                    size_hint_y: None
                    height: 150
                TextInput:
                    id: invoices
                    multiline: True
                    size_hint_y: None
                    height: 150
            Label:
                id: count
                size_hint_y: None
                height: 50
                text: ''
            ScrollView:
                size_hint: 0.5, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                GridLayout:
                    id: scroll_view
                    cols: 1
                    padding: 50
                    spacing: 50
                    size_hint_y: None
                    height: self.minimum_height
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: 80
                padding: 50
                spacing: 50
                MDRaisedButton:
                    text: 'ingest'
                    size_hint_y: None
                    height: 80
                    width: 200
                    on_release: root.do_ingest(invoices.text)

''')
Builder.load_string('''
<CloseChannel>:
    title: 'Close Channel'
    size: (800, 600)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    GridLayout:
        cols: 1
        row_force_default: True
        row_default_height: 60
        padding: 50
        spacing: 50
        MDTextField:
            id: channel_point
            helper_text: 'Channel Point'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats_per_vbyte
            helper_text: 'Sats per v/byte'
            helper_text_mode: "persistent"
        MDRaisedButton:
            text: 'close'
            on_release: root.close_channel(channel_point.text, sats_per_vbyte.text)
            size_hint_x: None
            width: 100
            size_hint_y: 1
            md_bg_color: 0.3,0.3,0.3,1

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import App kivy.app.App
#:import os os
#:import RankingsFileChooser orb.screens.rankings.RankingsFileChooser
#:import pref_path orb.misc.utils.pref_path


<RankingsFileChooser>:
    title: 'Import DB'
    size_hint: [.7,.7]
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        FileChooserIconView:
            size_hint: [1,1]
            id: filechooser
            path: App.get_running_app().user_data_dir
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: dp(30)
            MDRaisedButton:
                text: 'Ingest'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.selected_path = filechooser.selection[-1]; root.dismiss()
            MDRaisedButton:
                text: 'Cancel'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.dismiss()


<RankingsExportPath>:
    title: 'Export Rankings DB'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: None, None
    width: dp(700)
    height: dp(200)
    BoxLayout:
        orientation: 'vertical'
        MDTextField:
            id: path
            text: pref_path('export') / 'path_finding.json'
            helper_text: 'Export path'
            helper_text_mode: "persistent"
        Splitter:
            horizontal: True
            height: dp(50)
            size_hint_y: None
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: dp(30)
            MDRaisedButton:
                text: 'Export'
                size_hint_x: None
                width: dp(30)
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.selected_path = path.text; root.dismiss()
            MDRaisedButton:
                text: 'Cancel'
                size_hint_x: None
                width: dp(30)
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.dismiss()

<Rankings>:
    title: ''
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [.9, .9]
    BoxLayout:
        id: box_layout
        orientation: 'vertical'
        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: False
                ActionGroup:
                    text: 'File' 
                    mode: 'spinner'
                    ActionButton:
                        text: 'Export DB'
                        on_release: root.export()
                    ActionButton:
                        text: 'Ingest DB'
                        on_release: root.ingest()
                ActionGroup:
                    text: 'Edit' 
                    mode: 'spinner'
                    ActionButton:
                        text: 'Copy PKs'
                        on_release: root.copy_pks()
                ActionPrevious:
                    title: 'Rankings'
                    app_icon: ''
                    with_previous: False


''')
Builder.load_string('''
#:import dp kivy.metrics.dp 


<BatchOpenScreen>:
    title: 'Batch Open'
    size: (dp(800), dp(500))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    MDTabs:
        id: tabs
        on_tab_switch: root.on_tab_switch(*args)
        Tab:
            title: 'ingest'
            BoxLayout:
                orientation: 'vertical'
                MDTextField:
                    id: pubkeys
                    text: ''
                    helper_text: 'Pubkey [, amount]'
                    helper_text_mode: "persistent"
                    size_hint_y: 1
                    multiline: True
                BoxLayout:
                    orientation: 'horizontal'
                    height: dp(60)
                    size_hint_y: None
                    MDTextField:
                        id: amount
                        text: '100_000_000'
                        helper_text: 'Total amount in sats'
                        helper_text_mode: "persistent"
                        height: dp(60)
                        width: dp(200)
                        size_hint: (None, None)
                    MDRaisedButton:
                        text: 'Calculate Amounts'
                        on_release: root.calculate(pubkeys.text, amount.text)
                        size_hint_x: None
                        width: dp(100)
                        height: dp(40)
                        md_bg_color: 0.3,0.3,0.3,1
                    MDRaisedButton:
                        text: 'Ingest'
                        on_release: root.ingest(pubkeys.text)
                        size_hint_x: None
                        width: dp(100)
                        height: dp(40)
                        md_bg_color: 0.3,0.3,0.3,1
        Tab:
            title: 'connect'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                MDTextField:
                    id: connect
                    text: ''
                    helper_text: 'Connection Status'
                    helper_text_mode: "persistent"
                    size_hint_y: 1
                    multiline: True
                    size_hint: (1, 1)
                MDRaisedButton:
                    text: 'Connect'
                    on_release: root.batch_connect()
                    size_hint: (None, None)
                    width: dp(100)
                    height: dp(40)
                    md_bg_color: 0.3,0.3,0.3,1
        Tab:
            title: 'confirm'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                BoxLayout:
                    id: table_layout
                    orientation: 'vertical'
                    size_hint: (1, 1)
        Tab:
            title: 'open'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                MDTextField:
                    id: open_status
                    text: ''
                    helper_text: 'Open Status'
                    helper_text_mode: "persistent"
                    size_hint_y: 1
                    multiline: True
                    size_hint: (1, 1)
                MDRaisedButton:
                    text: 'Open'
                    on_release: root.batch_open()
                    size_hint: (None, None)
                    width: dp(100)
                    height: dp(40)
                    md_bg_color: 0.3,0.3,0.3,1

<Tab>

''')
Builder.load_string('''
########################################################################################
# NEW ADDRESS
########################################################################################

<NewAddress>:
    title: "New Wallet Address"
    size: (800,550)
    size_hint: (None, None)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0

    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 20
        MDTextField:
            id: address
            height: 120
            size_hint: (1, None)
        Image:
            id: img
            source: ''
''')
Builder.load_string('''
########################################################################################
# CONNECT
########################################################################################

<ConnectScreen>:
    name: 'connect'
    title: 'Connect'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    size: [600, 400]
    GridLayout:
        cols: 1
        row_force_default: True
        row_default_height: 60
        padding: 50
        spacing: 50
        MDTextField:
            id: address
            helper_text: 'Address'
            helper_text_mode: "persistent"
        MDRaisedButton:
            text: 'Connect'
            size_hint_x: None
            width: 30
            size_hint_y: 1
            md_bg_color: 0.3,0.3,0.3,1
            on_release: root.connect(address.text)

''')
Builder.load_string('''
########################################################################################
# OPEN CHANNEL
########################################################################################

<OpenChannelScreen>:
    title: 'Open Channel'
    size: (800, 600)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    GridLayout:
        cols: 1
        row_force_default: True
        row_default_height: 60
        padding: 50
        spacing: 50
        MDTextField:
            id: pk
            helper_text: 'Pubkey'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats
            helper_text: 'Sats'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats_per_vbyte
            helper_text: 'Sats per v/byte'
            helper_text_mode: "persistent"
        MDRaisedButton:
            text: 'open'
            on_release: root.open_channel(pk.text, sats.text, sats_per_vbyte.text)
            size_hint_x: None
            width: 100
            size_hint_y: 1
            md_bg_color: 0.3,0.3,0.3,1

''')
Builder.load_string('''
########################################################################################
# INVOICE
########################################################################################

#:import datetime datetime.datetime


<Invoice>
    orientation: 'vertical'
    size_hint_y: None
    height: 300
    padding: 10
    spacing: 10
    canvas.before:
        Color:
            rgba: 55 / 255, 55 / 255, 55 / 255, 0.5
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: 40
        Label:
            text: 'Raw: '
            height: 40
            width: 200
            size_hint_y: None
            size_hint_x: None
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            size_hint_y: None
            height: 40
            text: root.destination[:10] + '...'
            halign: "left"
            valign: "middle"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: 40
        Label:
            text: 'Amount: '
            height: 40
            width: 200
            size_hint_y: None
            size_hint_x: None
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            size_hint_y: None
            height: 40
            text: f'S{int(root.num_satoshis):,}'
            halign: "left"
            valign: "middle"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: 40
        Label:
            text: 'Expires in: '
            height: 40
            width: 200
            size_hint_y: None
            size_hint_x: None
            valign: "middle"
            halign: "left"
            text_size: self.size
        Label:
            id: expiry_label
            size_hint_y: None
            height: 40
            valign: "middle"
            halign: "left"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: 40
        Label:
            text: 'Description: '
            height: 40
            width: 200
            size_hint_y: None
            size_hint_x: None
            valign: "middle"
            halign: "left"
            text_size: self.size
        Label:
            size_hint_y: None
            height: 40
            text: root.description[:50]
            valign: "middle"
            halign: "left"
            text_size: self.size


''')
Builder.load_string('''
#:import dp kivy.metrics.dp

<SpinnerOption>:
    size_hint: None, None
    size: dp(400), dp(25)

<PayScreen>:
    title: 'Pay Invoices'
    size: (dp(400), dp(400))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            horizontal: True
        MDTextField:
            id: fee_rate
            text: str(500)
            helper_text: 'Fee Rate PPM'
            helper_text_mode: "persistent"
        MDTextField:
            id: num_threads
            text: str(3)
            helper_text: 'Threads'
            helper_text_mode: "persistent"
        MDTextField:
            id: max_paths
            text: str(10)
            helper_text: 'Max Paths'
            helper_text_mode: "persistent"
        Label:
            text: "First Hop Channel"
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: dp(25)
            canvas.before:
                PushMatrix
                Scale:
                    origin: self.center
                    xyz: .5, .5, 1
            canvas.after:
                PopMatrix
        Spinner:
            id: spinner_id
            text: 'any'
            height: dp(25)
            size_hint_y: 0
            size_hint_x: 1
            on_text: root.first_hop_spinner_click(spinner_id.text)
        Splitter:
            horizontal: True
        MDRaisedButton:
            text: 'Pay'
            font_size: '12sp'
            on_release: root.pay() 
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window

<SendCoins>:
    title: "Send Coins"
    size: min(dp(500), Window.size[0]), min(dp(500), Window.size[1])
    size_hint: (None, None)

    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 20
        Label:
            id: fees
            height: dp(120)
            size_hint_y: None
            text: "Fetching fees..."
        MDTextField:
            id: address
            height: dp(120)
            size_hint: (1, None)
            helper_text: 'Address'
            helper_text_mode: "persistent"
        MDTextField:
            id: amount
            height: dp(120)
            size_hint: (1, None)
            helper_text: 'Amount (Sats)'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats_per_vbyte
            height: dp(120)
            size_hint: (1, None)
            helper_text: 'Sats per v/byte'
            helper_text_mode: "persistent"
        MDRaisedButton:
            id: send_button
            text: "Send"
            on_release: root.send_coins(addr=address.text, amount=amount.text, sat_per_vbyte=sats_per_vbyte.text)

''')
Builder.load_string('''
<Rebalance>:
    title: 'Rebalance'
    size: (800, 900)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            horizontal: True
        MDTextField:
            id: amount
            text: '1_000_000'
            helper_text: 'Sats'
            helper_text_mode: "persistent"
        MDTextField:
            id: fee_rate
            text: str(500)
            helper_text: 'Fee Rate PPM'
            helper_text_mode: "persistent"
        MDTextField:
            id: max_paths
            text: str(100)
            helper_text: 'Max Paths'
            helper_text_mode: "persistent"
        Label:
            text: "First Hop Channel"
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: 60
            canvas.before:
                PushMatrix
                Scale:
                    origin: self.center
                    xyz: .5, .5, 1
            canvas.after:
                PopMatrix
        Spinner:
            id: spinner_out_id
            text: 'any'
            height: 60
            size_hint_y: 0
            size_hint_x: 1
            on_text: root.first_hop_spinner_click(spinner_out_id.text)
        Label:
            text: "Last Hop Pubkey"
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: 60
            canvas.before:
                PushMatrix
                Scale:
                    origin: self.center
                    xyz: .5, .5, 1
            canvas.after:
                PopMatrix
        Spinner:
            id: spinner_in_id
            text: 'any'
            height: 60
            size_hint_y: 0
            size_hint_x: 1
            on_text: root.last_hop_spinner_click(spinner_in_id.text)
        Splitter:
            horizontal: True
        Button:
            text: 'Rebalance'
            font_name: 'DejaVuSans'
            font_size: '12sp'
            on_release: root.rebalance() 
            size_hint_y: None
            height: 60

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import App kivy.app.App
#:import os os

<ConsoleFileChooser>:
    title: 'Open File'
    size_hint: [.7,.7]
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        FileChooserIconView:
            size_hint: [1,1]
            id: filechooser
            path: App.get_running_app().user_data_dir
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: dp(30)
            MDRaisedButton:
                text: 'Open'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.selected_path = filechooser.selection[-1]; root.dismiss()
            MDRaisedButton:
                text: 'Cancel'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.dismiss()
<ConsoleInput>:
    id: text_input
    disabled: False
    multiline: True
    size_hint_y: 1
    background_color: (14/255,14/255,15/255,255/255) if self.focus else (13/255,13/255,14/255,255/255)

<ConsoleOutput>:
    id: console_output
    text: root.output
    foreground_color: (0.9, 0.9, 0.9, 1)
    multiline: True
    size_hint_y: 1
    background_color: (14/255,14/255,15/255,255/255) if self.focus else (13/255,13/255,14/255,255/255)

<ConsoleSplitter@Splitter>:
    horizontal: True
    height: 10
    size_hint_y: None

<ConsoleScreen>:
    name: 'console'
    # BoxLayout:
    #     orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        ConsoleInput:
            id: console_input
        ConsoleSplitter:
            input: console_input
            output: console_output
        ConsoleOutput:
            id: console_output
        # BoxLayout:
        #     id: vid_box

''')
Builder.load_string('''

<PopupDropShadow@Popup>:
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    canvas.before:
        BorderImage:
            source: 'orb/images/shadow_inverted.png'
            border: 0,0,0,0
            pos: self.x + 10, self.y - 30
            size: self.width * 1.025, self.height * 1.025
''')
Builder.load_string('''
#:import dp kivy.metrics.dp

########################################################################################
# STATUS LINE IO
########################################################################################

<StatusLineOutput>
    text: root.output
    multiline: True
    size_hint: 0, 1
    width: self.texture_size[0]
    halign: "left"
    valign: "top"


########################################################################################
# STATUS LINE
########################################################################################

<StatusLine>
    id: status_line
    height: dp(25)
    size_hint_y: None
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: 55 / 255, 55 / 255, 55 / 255, 1
        Rectangle:
            pos: self.pos
            size: self.size
    MDRaisedButton:
        text: 'se'
        size_hint_x: None
        width: dp(25)
        size_hint_y: 1
        md_bg_color: 0.3,0.3,0.3,1
        on_release: app.root.ids.sm.current = 'console'
    StatusLineOutput:
        id: line_output

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import pref orb.misc.utils.pref
#:import Window kivy.core.window.Window
#:import Clipboard kivy.core.clipboard.Clipboard


<ConnectionSettings>:
    title: 'LND Node Connection Settings'
    size: min(dp(800), Window.size[0]), min(dp(500), Window.size[1])
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    MDTabs:
        id: tabs
        on_tab_switch: root.on_tab_switch(*args)
        Tab:
            title: 'Address'
            BoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: 'Enter the IP address or hostname of your LND node. It should not be an FQDN (e.g it should not contain https:// etc.).'
                    size_hint_y: 1
                    multiline: True
                BoxLayout:
                    orientation: 'horizontal'
                    height: dp(60)
                    size_hint_y: None
                    MDTextField:
                        id: address
                        text: pref('lnd.hostname')
                        helper_text: 'Host Address'
                        helper_text_mode: "persistent"
                        height: dp(60)
                        width: dp(200)
                        size_hint: (None, None)
                    MDRaisedButton:
                        text: 'Save'
                        on_release: root.set_and_save('lnd.hostname', address.text)
                        size_hint_x: None
                        width: dp(100)
                        height: dp(40)
                        md_bg_color: 0.3,0.3,0.3,1
                MDLabel:
                    text: 'Once save, you can proceed onto the next tab.'
                    size_hint_y: 1
        Tab:
            title: 'Protocol'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                MDLabel:
                    text: 'Enter the protocol for your LND node. If you are on a desktop, you man use GRPC. On mobile, you must select REST.'
                    size_hint_y: 1
                    multiline: True
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'vertical'
                        MDSwitch:
                            id: rest
                            on_release: root.save_protocol('rest')
                            active: pref('lnd.protocol') == 'rest'
                        MDLabel:
                            text: 'REST'
                    BoxLayout:
                        orientation: 'vertical'
                        MDSwitch:
                            id: grpc
                            on_release: root.save_protocol('grpc')
                            active: pref('lnd.protocol') == 'grpc'
                        MDLabel:
                            text: 'GRPC'
                    BoxLayout:
                        orientation: 'vertical'
                        MDSwitch:
                            id: mock
                            on_release: root.save_protocol('mock')
                            active: pref('lnd.protocol') == 'mock'
                        MDLabel:
                            text: 'MOCK'
                MDLabel:
                    text: 'Once entered, you can proceed onto the next tab.'
                    size_hint_y: 1
        Tab:
            title: 'Port'
            BoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: 'Enter the port # to connect your LND node. This is typically 8080 for REST, and 10009 for GRPC.'
                    size_hint_y: 0.1
                    multiline: True
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 0.8
                    MDTextField:
                        id: rest_port
                        text: str(int(pref('lnd.rest_port')))
                        helper_text: 'REST Port #'
                        helper_text_mode: "persistent"
                        height: dp(60)
                        width: dp(200)
                        size_hint: (None, None)
                    MDTextField:
                        id: grpc_port
                        text: str(int(pref('lnd.grpc_port')))
                        helper_text: 'GRPC Port #'
                        helper_text_mode: "persistent"
                        height: dp(60)
                        width: dp(200)
                        size_hint: (None, None)
                    MDRaisedButton:
                        text: 'Save'
                        on_release: (root.set_and_save('lnd.rest_port', rest_port.text), root.set_and_save('lnd.grpc_port', grpc_port.text))
                        size_hint_x: None
                        width: dp(100)
                        height: dp(40)
                        md_bg_color: 0.3,0.3,0.3,1
                MDLabel:
                    text: 'Once saved, you can proceed onto the next tab.'
                    size_hint_y: 0.1
        Tab:
            title: 'TLS Certificate'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                MDLabel:
                    text: "Install the 'rsa' module on your node, with pip3 install rsa then copy and run the provided command on your node."
                    size_hint_y: 0.3
                    multiline: True
                MDIconButton:
                    icon: "content-copy"
                    size_hint_y: 0.2
                    on_release: root.copy_cert_encrypt_command()
                TextInput:
                    id: tls_cert
                    text: root.get_cert()
                    on_text: root.validate_cert(self.text)
                    size_hint_y: 0.4
                    multiline: True
                    size_hint: (1, 1)
                MDLabel:
                    id: feedback
                    text: ""
                    size_hint_y: 0.1
                    multiline: True
                MDRaisedButton:
                    text: 'Save'
                    on_release: root.save_cert(tls_cert.text)
                    size_hint: (None, None)
                    width: dp(100)
                    height: dp(40)
                    md_bg_color: 0.3,0.3,0.3,1
                MDLabel:
                    text: 'Once saved, you can proceed onto the next tab.'
                    size_hint_y: 0.1
        Tab:
            title: 'Macaroon'
            BoxLayout:
                orientation: 'vertical'
                size_hint: (1, 1)
                MDLabel:
                    text: "Install the 'rsa' module on your node (if you haven't already) with pip3 install rsa then copy and run the provided command on your node."
                    size_hint_y: 0.3
                    multiline: True
                MDIconButton:
                    icon: "content-copy"
                    size_hint_y: 0.2
                    on_release: root.copy_mac_encrypt_command()
                TextInput:
                    id: macaroon
                    text: root.get_macaroon()
                    helper_text: 'Macaroon'
                    helper_text_mode: "persistent"
                    on_text: root.validate_macaroon(self.text)
                    size_hint_y: 0.4
                    multiline: True
                    size_hint: (1, 1)
                MDLabel:
                    id: mac_feedback
                    text: ""
                    size_hint_y: 0.1
                    multiline: True
                MDRaisedButton:
                    text: 'Save'
                    on_release: root.save_macaroon(macaroon.text)
                    size_hint: (None, None)
                    width: dp(100)
                    height: dp(40)
                    md_bg_color: 0.3,0.3,0.3,1

<Tab>

''')
Builder.load_string('''
<PlayerDialog>:
    title: 'player'
    size_hint: .8, .8
    MDTabs:
        id: tabs
        on_tab_switch: root.on_tab_switch(*args)
        Tab:
            title: 'Collections'
            ScrollView:
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                GridLayout:
                    id: collections
                    cols: 3
                    row_force_default: True
                    row_default_height: dp(360/2)
                    padding: 20
                    spacing: 20
        Tab:
            title: 'Videos'
            ScrollView:
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                GridLayout:
                    id: videos
                    cols: 3
                    row_force_default: True
                    row_default_height: dp(360/2)
                    padding: 20
                    spacing: 20
                    size_hint_y: None
                    height: self.minimum_height
                    Label:
                        text: "Please first select a collection"
        Tab:
            title: 'Player'
            BoxLayout:        
                id: bl
                orientation: 'vertical'
                Label:
                    text: "Please first select a video"

<Tab>

<CollectionWidget>
    Button:
        id: button
        size: dp(640/2), dp(360/2)
        size_hint: None, None
        Image:
            source: 'images/overview.png'
            y: self.parent.y
            x: self.parent.x
            size: [self.parent.size[0], self.parent.size[1]]
            allow_stretch: True

<VideoWidget>
    Button:
        id: button
        size: dp(640/2), dp(360/2)
        Image:
            source: 'images/overview_blank.png'
            y: self.parent.y
            x: self.parent.x
            size: [self.parent.size[0], self.parent.size[1]]
            allow_stretch: True
        Label:
            text: root.title
            markup: True
            multiline: True
            pos: (root.pos[0]+root.size[0]/2, root.pos[1]+root.size[1]/3)
            font_size: '24sp'
            halign: "left"
            valign: "middle"
            text_size: root.size

''')
Builder.load_string('''
#:import dp kivy.metrics.dp

<FeeDistribution>:
    title: "Fee Distribution"
    size_hint: (.9, .9)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0

    BoxLayout:
        orientation: 'vertical'
        Label:
            id: alias
            size_hint_y: None
            height: dp(12)
        BoxLayout:
            orientation: 'horizontal'
            BoxLayout:
                id: bl
                orientation: 'horizontal'
            BoxLayout:
                id: table
                orientation: 'horizontal'

        MDRaisedButton:
            text: 'Next Channel'
            on_release: root.next_channel()
            size_hint_x: None
            width: dp(100)
            height: dp(40)
            md_bg_color: 0.3,0.3,0.3,1
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window

<FocusTextInput>:

<MailDialog>:
    title: 'Keysend Mail'
    size_hint: .8, .8
    FocusTextInput:
        id: input
        size_hint_x: 0.8

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import pref orb.misc.utils.pref
#:import Window kivy.core.window.Window
#:import TipDialog orb.dialogs.app_store.TipDialog


<StarButton@MDIconButton>
    icon: "star"
    on_release: self.icon = "star-outline" if self.icon == "star" else "star"


<AppStoreDialog>:
    title: 'App Store'
    size: min(dp(800), Window.size[0]), min(dp(500), Window.size[1])
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    MDTabs:
        id: tabs
        on_tab_switch: root.on_tab_switch(*args)
        Tab:
            title: 'Installed'
            ScrollView:
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                MDList:
                    padding: dp(50)
                    id: installed
        Tab:
            title: 'Available'
            ScrollView:
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                MDList:
                    padding: dp(50)
                    id: available
        Tab:
            title: 'Details'
            id: details


<Tab>

''')
Builder.load_string('''
#:import TipDialogContent orb.dialogs.app_store.TipDialogContent
#:import Lnd orb.lnd.Lnd

<TipDialogContent>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "250dp"

    MDTextField:
        hint_text: "Author Alias"
        text: Lnd().get_node_alias(root.app.author)
        disabled: True

    MDTextField:
        hint_text: "Author PubKey"
        text: root.app.author
        disabled: True

    MDTextField:
        id: sats
        text: '1000'
        hint_text: "Sats"

    MDTextField:
        id: message
        text: 'Thanks for your great ' + root.app.name +' app!'
        hint_text: "Message"

<TipDialog>
    title: 'Tip App Author'
    type: 'custom'
    md_bg_color: .1, .1, .15, .9
    overlay_color: 0, 0, 0, 0
    canvas.before:
        BorderImage:
            source: 'orb/images/shadow_inverted.png'
            border: 0,0,0,0
            pos: self.x + 10, self.y - 30
            size: self.width * 1.025, self.height * 1.025

''')
Builder.load_string('''


<AppDetails>:
    orientation: "vertical"
    size_hint: 1, None
    height: box_top.height + box_center.height + box_bottom.height
    focus_behavior: True
    ripple_behavior: True
    pos_hint: {"center_x": .5, "center_y": .5}

    MDBoxLayout:
        id: box_top
        spacing: "20dp"
        adaptive_height: True

        MDBoxLayout:
            id: text_box
            orientation: "horizontal"
            adaptive_height: True
            AnchorLayout:
                size_hint_x: .2
                anchor_x: 'center'
                anchor_y: 'center'
                AsyncImage:
                    size_hint: None, None
                    size: "80dp", "60dp"
                    keep_ratio: True
                    source: root.app.icon if hasattr(root.app, 'icon') else ''
            MDBoxLayout:
                id: text_box
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: 0, "10dp", "10dp", "10dp"
                MDLabel:
                    text: root.app.name
                    theme_text_color: "Primary"
                    font_style: "H5"
                    bold: True
                    adaptive_height: True
                MDLabel:
                    text: root.app.description
                    adaptive_height: True
                    theme_text_color: "Primary"

    MDSeparator:

    MDBoxLayout:
        id: box_center
        adaptive_height: True
        padding: "10dp", 0, 0, 0

        MDLabel:
            text: "Rate this app"
            adaptive_height: True
            pos_hint: {"center_y": .5}
            theme_text_color: "Primary"

        StarButton:
        StarButton:
        StarButton:
        StarButton:
        StarButton:

    MDSeparator:

    MDBoxLayout:
        id: box_bottom
        adaptive_height: True
        padding: "10dp"
        spacing: "10dp"

        MDRaisedButton:
            id: install_button
            text: "Uninstall" if root.app.installed else "Install"
            on_release: root.install_uninstall()

        MDRaisedButton:
            id: tip_button
            text: "Tip author.."
            on_release: TipDialog(app=root.app).open()
            disabled: root.app.is_remote

        # MDRaisedButton:
        #     id: delete_button
        #     text: "Delete app from store"
        #     on_release: root.delete_app()

''')
Builder.load_string('''

<AppSummary>:
    orientation: "vertical"
    size_hint: .5, None
    height: box_top.height + box_bottom.height
    focus_behavior: True
    ripple_behavior: True
    pos_hint: {"center_x": .5, "center_y": .5}

    MDBoxLayout:
        id: box_top
        spacing: "20dp"
        adaptive_height: True

        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            spacing: "10dp"
            padding: 0, "10dp", "10dp", "10dp"
            AnchorLayout:
                size_hint_x: .2
                anchor_x: 'center'
                anchor_y: 'center'
                AsyncImage:
                    size_hint: None, None
                    size: "80dp", "60dp"
                    keep_ratio: True
                    source: root.app.icon if hasattr(root.app, 'icon') else ''
            MDBoxLayout:
                id: text_box
                size_hint_x: .8
                orientation: "vertical"
                adaptive_height: True
                spacing: "10dp"
                padding: 0, "10dp", "10dp", "10dp"
                MDLabel:
                    text: root.app.name
                    theme_text_color: "Primary"
                    font_style: "H5"
                    bold: True
                    adaptive_height: True
                MDLabel:
                    text: root.app.description
                    adaptive_height: True
                    theme_text_color: "Primary"

    MDSeparator:

    MDBoxLayout:
        id: box_bottom
        adaptive_height: True
        padding: "10dp", 0, 0, 0

        MDLabel:
            text: "Rate this app"
            adaptive_height: True
            pos_hint: {"center_y": .5}
            theme_text_color: "Primary"

        StarButton:
        StarButton:
        StarButton:
        StarButton:
        StarButton:

''')
Builder.load_string('''
#:import TipDialogContent orb.dialogs.app_store.TipDialogContent
#:import Lnd orb.lnd.Lnd

<LoginDialogContent>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "250dp"

    MDTextField:
        hint_text: "Pubkey"
        text: root.pk
        # disabled: True

    MDTextField:
        hint_text: "Password"
        text: root.password
        # disabled: True

    MDTextField:
        hint_text: "Token"
        text: root.token
        # disabled: True

<LoginDialog>
    title: 'App Store Login'
    type: 'custom'
    md_bg_color: .1, .1, .15, .9
    overlay_color: 0, 0, 0, 0
    canvas.before:
        BorderImage:
            source: 'orb/images/shadow_inverted.png'
            border: 0,0,0,0
            pos: self.x + 10, self.y - 30
            size: self.width * 1.025, self.height * 1.025

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window

<IconListItem>
    IconLeftWidget:
        icon: root.icon



<UploadAppDialog>:
    title: 'Upload App'
    size_hint: .5, .5
    BoxLayout:
        orientation: "vertical"
        padding: "10dp"
        spacing: "10dp"
        adaptive_height: True
        Label:
            text: "Please select app you wish to upload."
            size_hint_y: 0.1
        MDDropDownItem:
            id: drop_item
            pos_hint: {'center_x': .5, 'center_y': .5}
            text: 'Select App'
            on_release: root.menu.open()
        ScrollView:
            size_hint_x: 0.8
            padding: dp(50)
            spacing: dp(50)
            pos_hint: {'center_x': .5, 'center_y': .5}
            Label:
                id: output
                size_hint: None, None
                size: self.texture_size
                multiline: True
        BoxLayout:
            orientation: 'horizontal'
            spacing: '10dp'
            padding: '10dp'
            size_hint_y: 0.1
            MDRaisedButton:
                text: "Sign"
                on_release: root.sign()
                disabled: True
                md_bg_color_disabled: .2,.2,.2,1
            MDRaisedButton:
                id: archive_button
                text: "Archive"
                on_release: root.archive()
                disabled: True
                md_bg_color_disabled: .2,.2,.2,1
            MDRaisedButton:
                id: upload_button
                text: "Upload"
                on_release: root.upload()
                disabled: True
                md_bg_color_disabled: .2,.2,.2,1
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window

<ReleaseNotes>:
    title: 'Release Notes'
    size: min(dp(800), Window.size[0]), min(dp(500), Window.size[1])
    size_hint: [None, None]
    ScrollView:
        size_hint: 1, 1
        padding: dp(50)
        spacing: dp(50)
        pos_hint: {'center_x': .5, 'center_y': .5}
        Label:
            id: release_notes
            size_hint: None, None
            size: self.texture_size
            multiline: True
''')
Builder.load_string('''
<About>:
    title: 'About'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    size: [600, 700]
    Label:
        size_hint: [1,1]
        text: 'Orb is being developed in the\
heart of the plebnet.\
\
Big thanks to:\
\
Miguel\
Richard\
Neski\
B\
\
And countless others for their\
time, input and knowledge.'
''')
Builder.load_string('''
#:kivy 2.0.0
#:import sp kivy.metrics.sp
#:import dp kivy.metrics.dp
#:import data_manager orb.misc.data_manager
#:import Lnd orb.lnd.Lnd
#:import MailDialog orb.dialogs.mail_dialog.MailDialog
#:import PlayerDialog orb.dialogs.player_dialog.PlayerDialog
#:import NewAddress orb.screens.new_address_screen.NewAddress
#:import SendCoins orb.screens.send_coins.SendCoins
#:import IngestInvoicesScreen orb.screens.ingest_invoices_screen.IngestInvoicesScreen
#:import PayScreen orb.screens.pay_screen.PayScreen
#:import ConnectScreen orb.screens.connect_screen.ConnectScreen
#:import OpenChannelScreen orb.screens.open_channel_screen.OpenChannelScreen
#:import BatchOpenScreen orb.screens.batch_open_screen.BatchOpenScreen
#:import CloseChannel orb.screens.close_channel.CloseChannel
#:import Rebalance orb.screens.rebalance.Rebalance
#:import prefs_col orb.misc.utils.prefs_col
#:import set_string_pref orb.misc.utils.set_string_pref
#:import view_forwarding_history orb.dialogs.forwarding_history.view_forwarding_history
#:import graph_fees_earned orb.dialogs.forwarding_history.graph_fees_earned
#:import FeeDistribution orb.dialogs.fee_distribution.FeeDistribution
#:import About orb.dialogs.help_dialog.about.about.About
#:import ReleaseNotes orb.dialogs.help_dialog.release_notes.release_notes.ReleaseNotes
#:import Rankings orb.screens.rankings.Rankings
#:import ConnectionSettings orb.dialogs.connection_settings.ConnectionSettings
#:import AppStoreDialog orb.dialogs.app_store.AppStoreDialog
#:import LoginDialog orb.dialogs.app_store.LoginDialog
#:import UploadAppDialog orb.dialogs.upload_app.UploadAppDialog

#: import webbrowser webbrowser
########################################################################################
# MAIN
########################################################################################


<MainLayout@BoxLayout>:
    # This is the main UI Layout KV. This is where a lot of the
    # top-level UI magic happens.
    id: main_layout
    menu_visible: any([view_context_menu.visible, scripts_context_menu.visible, app_context_menu.visible, lightning_context_menu.visible, help_context_menu.visible, onchain_context_menu.visible])
    orientation: 'vertical'
    # hack alert: the submenus are pretty buggy, and require
    # us to build them at the bottom off the screen then moving
    # them to the top. So we build this widget upside down and
    # then flip it.
    StatusLine
        id: status_line
    ScreenManager:
        # In case we have many screens, well we have a screen
        # manager to easily go from one screen to another.
        # might be a good idea to get rid of this as it may 
        # introduce a lot of unecessary complexity, and most
        # things seem to work well as dialogs in Kivy. 
        id: sm
        ChannelsScreen:
            id: channels
        ConsoleScreen
    TopMenu:
        id: app_menu
        top: root.height
        cancel_handler_widget: main_layout
        AppMenuTextItem:
            text: "View"
            ContextMenu:
                id: view_context_menu
        AppMenuTextItem:
            text: "Lightning"
            ContextMenu:
                id: lightning_context_menu
                ContextMenuTextItem:
                    text: "Channels"
                    on_release: app_menu.close_all()
                    on_press: app.root.ids.sm.current = 'channels'
                ContextMenuTextItem:
                    text: "Pay"
                    on_release: app_menu.close_all()
                    on_press:  PayScreen().open()
                ContextMenuTextItem:
                    text: "Rebalance"
                    on_release: app_menu.close_all()
                    on_press:  Rebalance().open()
                ContextMenuTextItem:
                    text: "Mail"
                    on_press:  app_menu.close_all()
                    on_release: MailDialog().open()
                ContextMenuTextItem:
                    text: "Open Channel"
                    on_press:  OpenChannelScreen().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Batch Open"
                    on_press:  BatchOpenScreen().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Close Channel"
                    on_press:  CloseChannel().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Connect"
                    on_press:  ConnectScreen().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Ingest Invoices"
                    on_press: IngestInvoicesScreen().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Rankings"
                    on_press: Rankings().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Forwarding History"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "Total Routing"
                            on_release: (app_menu.close_all(), view_forwarding_history())
                        ContextMenuTextItem:
                            text: "Fees Earned"
                            on_release: (app_menu.close_all(), graph_fees_earned())
                        ContextMenuTextItem:
                            text: "Fee Distribution"
                            on_release: (app_menu.close_all(), FeeDistribution().open())
                ContextMenuTextItem:
                    text: "Sort Channels"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "ratio"
                            on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'ratio'))
                        ContextMenuTextItem:
                            text: "capacity"
                            on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'capacity'))
                        ContextMenuTextItem:
                            text: "total-sent"
                            on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'total-sent'))
                        ContextMenuTextItem:
                            text: "total-received"
                            on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'total-received'))
                        ContextMenuTextItem:
                            text: "out-ppm"
                            on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'out-ppm'))


        AppMenuTextItem:
            text: "On-Chain"
            ContextMenu:
                id: onchain_context_menu
                ContextMenuTextItem:
                    text: "New Address"
                    on_press: app_menu.close_all()
                    on_release: NewAddress().open()
                ContextMenuTextItem:
                    text: "Send Coins"
                    on_press: app_menu.close_all()
                    on_release: SendCoins().open()
        AppMenuTextItem:
            text: "Orb"
            ContextMenu:
                id: app_context_menu
                ContextMenuTextItem:
                    text: "Settings"
                    on_press: app_menu.close_all()
                    on_release: app.open_settings()
                ContextMenuTextItem:
                    text: "Connection Settings"
                    on_press: ConnectionSettings().open()
                    on_release: app_menu.close_all()
                ContextMenuDivider
                ContextMenuTextItem:
                    text: "App Store Login"
                    on_press: LoginDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "App Store"
                    on_press: AppStoreDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Upload App"
                    on_press: UploadAppDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuDivider
                ContextMenuTextItem:
                    text: "Files"
                    on_press: app_menu.close_all()
                    on_release: webbrowser.open('file://' + App.get_running_app().user_data_dir)
                ContextMenuTextItem:
                    text: "Console"
                    on_press:  app.root.ids.sm.current = 'console'
                    on_release: app_menu.close_all()
                # ContextMenuTextItem:
                #     text: "Player"
                #     on_press:  app_menu.close_all()
                #     on_release: PlayerDialog().open()
                ContextMenuDivider
                ContextMenuTextItem:
                    text: "Quit"
                    on_press: app_menu.close_all()
                    on_release: app.get_running_app().stop()
        AppMenuTextItem:
            text: "Apps"
            id: scripts
            ContextMenu:
                id: scripts_context_menu
        AppMenuTextItem:
            text: "Help"
            ContextMenu:
                id: help_context_menu
                ContextMenuTextItem:
                    text: "About"
                    on_press: app_menu.close_all()
                    on_release: About().open()
                ContextMenuTextItem:
                    text: "Release Notes"
                    on_press: app_menu.close_all()
                    on_release: ReleaseNotes().open()
                ContextMenuTextItem:
                    text: "Links"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "Terminal"
                            on_release: webbrowser.open("https://terminal.lightning.engineering/#/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "Amboss"
                            on_release: webbrowser.open("https://amboss.space/node/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "LNRouter"
                            on_release: webbrowser.open("https://lnrouter.app/node/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "LNNodeInsight"
                            on_release: webbrowser.open("https://lnnodeinsight.com/")
                        ContextMenuTextItem:
                            text: "1ML"
                            on_release: webbrowser.open("https://1ml.com/node/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "HashXP"
                            on_release: webbrowser.open("https://hashxp.org/lightning/node/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "LN.plus"
                            on_release: webbrowser.open("https://lightningnetwork.plus/nodes/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "CheeseRobot"
                            on_release: webbrowser.open("https://cheeserobot.org/node/" + Lnd().get_info().identity_pubkey)
                        ContextMenuTextItem:
                            text: "Acinq"
                            on_release: webbrowser.open("https://explorer.acinq.co/n/" + Lnd().get_info().identity_pubkey)

''')
Builder.load_string('''

''')
Builder.load_string('''
#:import pref orb.misc.utils.pref


<Node@Button>
    background_color: (0, 0, 0, 0)
    size_hint: None, None
    size: (root.width_pref+2, root.height_pref+2)
    background_normal: ''
    font_size: pref('display.node_alias_font_size')
    canvas.before:
        Color: 
            rgba: (0.3,0.3,0.9,1)
        RoundedRectangle:
            size: (root.width_pref+2, root.height_pref+2)
            pos: [self.pos[0]-1, self.pos[1]-1]
            radius: [(8, 50)[bool(root.round)]]
        Color: 
            rgba: root.col
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [(8, 50)[bool(root.round)]]
            size: (root.width_pref, root.height_pref)
        PushMatrix
        Scale:
            origin: self.center
            xyz: .1, .1, 1
    canvas.after:
        PopMatrix

''')
Builder.load_string('''
#:import prefs_col orb.misc.utils.prefs_col
#:import pref orb.misc.utils.pref
#:import dp kivy.metrics.dp

<BorderedLabel>:
    canvas.before:
        Color:
            rgba: [ a*b for a,b in zip(prefs_col('display.channels_background_color'), [1,1,1,root.alpha*0.7])]
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, root.alpha
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1
''')
Builder.load_string('''
#:import prefs_col orb.misc.utils.prefs_col
#:import pref orb.misc.utils.pref
#:import dp kivy.metrics.dp



<HUDFeeSummary>:
    id: hud_label
    text: root.hud
    size_hint: [None, None]
    markup: True
    size: [self.texture_size[0]+40, self.texture_size[1]+30]

<HUDBalance>:
    id: hud_label
    text: root.hud
    size_hint: [None, None]
    markup: True
    size: [self.texture_size[0]+40, self.texture_size[1]+30]

<HUDDPI>:
    id: hud_label
    text: root.hud
    size_hint: [None, None]
    markup: True
    size: [self.texture_size[0]+40, self.texture_size[1]+30]

<HUDMempool>:
    id: hud_label
    text: root.hud
    size_hint: [None, None]
    markup: True
    size: [self.texture_size[0]+40, self.texture_size[1]+30]

<HUDThreadManager>:
    size_hint: [None, None]
    size: [300, (int(len(self.children) / 6) + 1) * dp(30)]
    padding: dp(10)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: [ a*b for a,b in zip(prefs_col('display.channels_background_color'), [1,1,1,root.alpha*0.7])]
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, root.alpha
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1


<HUDProtocol>:
    size_hint: [None, None]
    size: [dp(120), dp(30)]
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: prefs_col('display.channels_background_color')
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, 1
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1

<HUDGlobalRatio>:
    size_hint: [None, None]
    size: [dp(150), dp(30)]
    padding: dp(10), dp(10)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: [ a*b for a,b in zip(prefs_col('display.channels_background_color'), [1,1,1,root.alpha*0.7])]
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, root.alpha
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1

<HUDBTCPrice>:
    size_hint: [None, None]
    size: [300, 150]
    canvas.before:
        Color:
            rgba: [ a*b for a,b in zip(prefs_col('display.channels_background_color'), [1,1,1,root.alpha*0.7])]
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, root.alpha
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1
        Color:
            rgba: 1, 1, 1, 1
        PushMatrix
        Translate:
            xyz: self.pos[0], self.pos[1], 0
        Line:
            points: root.line_points
    canvas.after:
        PopMatrix
    Label:
        id: rate
        pos: [0, root.height - self.texture_size[1]-30]
        font_size: '10sp'
        size_hint: [None, None]
        markup: True
        size: [self.texture_size[0]+40, self.texture_size[1]+30]

<ThreadWidget>:
    Button:
        id: name
        font_size: '13sp'
        # size_hint: None, None
        size: dp(10), dp(10)
        text: root.thread.name[0]
        background_color: 0,0,0,0
        pos: root.pos
        on_release: root.thread.stop()

<HUDUIMode>:
    size_hint: [None, None]
    size: [dp(120), dp(30)]
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: prefs_col('display.channels_background_color')
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: .6, .6, .8, 1
        Line:
            points: [self.pos[0]+self.width, self.pos[1], self.pos[0]+self.width, self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0], self.pos[1] + self.height]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1]]
            width: 1
        Line:
            points: [self.pos[0], self.pos[1] + self.height, self.pos[0] + self.width, self.pos[1] + self.height]
            width: 1
''')
Builder.load_string('''
#:import prefs_col orb.misc.utils.prefs_col



<HUD>:
    anchor_x: 'left'
    anchor_y: 'top'
    size_hint: [1, 1]
    HUDSW
    HUDNW
    HUDSE
    HUDNE

<HUDNW>:
    anchor_x: 'left'
    anchor_y: 'top'
    BoxLayout:
        pos: root.pos
        size: root.size
        orientation: 'vertical'
        HUDBalance
        HUDGlobalRatio
        HUDFeeSummary
        Widget:

<HUDNE>:
    anchor_x: 'right'
    anchor_y: 'top'
    HUDMempool


<HUDSW>:
    anchor_x: 'left'
    anchor_y: 'bottom'
    BoxLayout:
        size_hint: [1, 1]
        orientation: 'vertical'
        HUDUIMode
        HUDProtocol
        HUDThreadManager
        HUDDPI


<HUDSE>:
    anchor_x: 'right'
    anchor_y: 'bottom'
    HUDBTCPrice

''')
Builder.load_string('''
<ChannelsWidget>:
    size_hint: 3, 3
    pos: [-self.width/10, -self.height/10]
    canvas:
        Color:
            rgba: 0, 1, 0, (0.1 * (app.config['debug']['layouts'] == '1'))
        Rectangle:
            size: self.size
    RelativeLayout:
        id: relative_layout
        size: [0, 0]
        pos: [root.size[0]/2, root.size[1]/2]
        size_hint: None, None
        canvas:
            Color:
                rgba: 1, 0, 0, (0.1 * (app.config['debug']['layouts'] == '1'))
            Rectangle:
                pos: self.pos
                size: self.size


<ChannelWidget>:

<FeeWidget>:



''')
Builder.load_string('''
#:import prefs_col orb.misc.utils.prefs_col
#:import Lnd orb.lnd.Lnd

<ChannelsScreen>:
    name: 'channels'
    FloatLayout:
        canvas:
            Color:
                rgba: prefs_col('display.channels_background_color')
            Rectangle:
                size: self.size
                pos: self.pos
        RelativeLayout:
            id: cw_layout
        Widget:
            id: gestures_overlay
            size_hint: 1, 1
        HUD:
            id: hud
        MDNavigationLayout:
            MDNavigationDrawer:
                anchor: "right"
                id: nav_drawer
                md_bg_color: 0, 0, 0, 0.5
                AttributeEditor:
                    id: content_drawer


<ItemDrawer>
    text_color: [1, 1, 1, 1]

    IconLeftWidget:
        id: icon
        icon: root.icon
        text_color: [1, 1, 1, 1]


''')
Builder.load_string('''
<FeeWidgetLabel>:
    font_size: '24sp'
    size: [self.texture_size[0]*0.2, self.texture_size[1]*.2]
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center
            xyz: .2, .2, 1
    canvas.after:
        PopMatrix
''')
Builder.load_string('''
<ContextMenu>:
    cols: 1
    size_hint: None, None
    spacing: 0, 0
    spacer: _spacer
    on_visible: self._on_visible(args[1])
    on_parent: self._on_visible(self.visible)

    Widget:
        id: _spacer
        size_hint: 1, None
        height: dp(3)
        canvas.before:
            Color:
                rgb: root.hl_color
            Rectangle:
                pos: self.pos
                size: self.size


<ContextMenuItem>:
    size_hint: None, None
    submenu_arrow: _submenu_arrow
    on_children: self._check_submenu()
    on_parent: self._check_submenu()
    canvas.before:
        Color:
            rgb: (0.15, 0.15, 0.15)
        Rectangle:
            pos: 0,0
            size: self.size

    Widget:
        id: _submenu_arrow
        size_hint: None, None
        width: dp(6)
        height: dp(11)
        pos: self.parent.width - self.width - dp(5), (self.parent.height - self.height) / 2
        canvas.before:
            Translate:
                xy: self.pos
            Color:
                rgb: (0.35, 0.35, 0.35) if self.disabled else (1, 1, 1)
            Triangle:
                points: [0,0, self.width,self.height/2, 0,self.height]
            Translate:
                xy: (-self.pos[0], -self.pos[1])


<ContextMenuText>:
    label: _label
    width: self.parent.width if self.parent else 0
    height: dp(26)
    font_size: '15sp'

    Label:
        pos: 0,0
        id: _label
        text: self.parent.text
        color: self.parent.color
        font_size: self.parent.font_size
        padding: dp(10), 0
        halign: 'left'
        valign: 'middle'
        size: self.texture_size
        size_hint: None, 1


<AbstractMenuItemHoverable>:
    on_hovered: self._on_hovered(args[1])
    canvas.before:
        Color:
            rgb: (0.25, 0.25, 0.25) if self.hovered and not self.disabled else (0.15, 0.15, 0.15)
        Rectangle:
            pos: 0,0
            size: self.size


<ContextMenuDivider>:
    font_size: '10sp'
    height: dp(20) if len(self.label.text) > 0 else dp(1)
    canvas.before:
        Color:
            rgb: (0.25, 0.25, 0.25)
        Rectangle:
            pos: 0,self.height - 1
            size: self.width, 1


<ContextMenuButton@Button>:
    size_hint: None, None
    font_size: '12sp'
    height: dp(20)
    background_normal: ""
    background_down: ""
    background_color: HIGHLIGHT_COLOR
    border: (0, 0, 0, 0)
    on_press: self.background_color = 0.10, 0.6, 0.8, 1.0
    on_release: self.background_color = HIGHLIGHT_COLOR


<ContextMenuToggleButton@ToggleButton>:
    size_hint: None, None
    font_size: '12sp'
    size: dp(30), dp(20)
    background_normal: ""
    background_down: ""
    background_color: HIGHLIGHT_COLOR if self.state == 'down' else (0.25, 0.25, 0.25, 1.0)
    border: (0, 0, 0, 0)
    on_press: self.background_color = 0.10, 0.6, 0.8, 1.0
    on_release: self.background_color = HIGHLIGHT_COLOR


<ContextMenuSmallLabel@Label>:
    size: self.texture_size[0], dp(18)
    size_hint: None, None
    font_size: '12sp'


<ContextMenuTextInput@TextInput>:
    size_hint: None, None
    height: dp(22)
    font_size: '12sp'
    padding: dp(7), dp(3)
    multiline: False

''')
Builder.load_string('''
<AppMenu>:
    height: dp(30)
    size_hint: 1, None

    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            pos: self.pos
            size: self.size


<AppMenuTextItem>:
    disabled: True
    size_hint: None, None
    on_children: self._check_submenu()
    font_size: '15sp'
    background_normal: ""
    background_down: ""
    background_color: root.hl_color if self.state == 'down' else (0.2, 0.2, 0.2, 1.0)
    background_disabled_normal: ""
    background_disabled_down: ""
    border: (0, 0, 0, 0)
    size: self.texture_size[0], dp(30)
    padding_x: dp(10)

''')