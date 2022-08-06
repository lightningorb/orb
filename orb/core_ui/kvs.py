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
        id: earned
        helper_text: 'Earned'
        helper_text_mode: 'persistent'

    MDTextField:
        id: helped_earn
        helper_text: 'Helped earn'
        helper_text_mode: 'persistent'

    MDTextField:
        id: profit
        helper_text: 'Profit'
        helper_text_mode: 'persistent'

    # MDTextField:
    #     id: debt
    #     helper_text: 'Debt'
    #     helper_text_mode: 'persistent'

    ScrollView:
        DrawerList:
            id: md_list

''')
Builder.load_string('''
#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp

<CloseChannel>:
    title: 'Close Channel'
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(300))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        height: self.minimum_height
        Label:
            text: "force"
            size_hint_y: None
            height: self.texture_size[1]
        MDCheckbox:
            id: force
        Widget:
        MDTextField:
            id: channel_point
            helper_text: 'Channel Point'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats_per_vbyte
            text: '1'
            helper_text: 'Sats per v/byte'
            helper_text_mode: "persistent"
        Widget:
        MDRaisedButton:
            text: 'close'
            on_release: root.close_channel(channel_point.text, sats_per_vbyte.text)
            size_hint: 1, None
            height: dp(50)

''')
Builder.load_string('''
<ImportConnectionSettings>:
    name: 'import_node_settings'
    BoxLayout:
        orientation: 'vertical'
        size_hint: (1, 1)
        MDTextField:
            id: device_id
            text: str(device_id().decode())
            helper_text: 'Device ID'
            helper_text_mode: "persistent"
            size_hint_x: None
            width: dp(200)
        TextInput:
            id: text_import
            multiline: True
        MDRaisedButton:
            text: 'Import'
            on_release: root.import_node_settings()
            size_hint: (None, None)
            width: dp(100)
            height: dp(40)
        MDRaisedButton:
            id: connect
            text: 'Connect'
            on_release: root.connect()
            size_hint_x: 1
            height: dp(40)
        MDRaisedButton:
            text: 'Back'
            on_release:
                app.screen.ids.sm.current = "main"
                root.manager.transition.direction = "right"
            size_hint_x: 1
            size_hint_y: None
            height: dp(40)

''')
Builder.load_string('''
#:import Factory kivy.factory.Factory
#:import get_available_nodes orb.misc.utils.get_available_nodes

<NodeSpinnerOption@SpinnerOption>:
    size_hint: None, None
    size: dp(300), dp(30)


<ExportConnectionSettings>:
    name: 'export_node_settings'
    BoxLayout:
        orientation: 'vertical'
        size_hint: (1, 1)
        Spinner:
            id: nodes
            # option_cls: Factory.get("NodeSpinnerOption")
            text: "Select node to export"
            height: dp(30)
            width: dp(300)
            size_hint: None, None
            on_text:
                root.node_selected(self.text)
            values: [x[:10] for x in get_available_nodes()]
        Label:
            text: "The device ID to export to"
            size_hint_y: None
            height: self.texture_size[1]
        MDTextField:
            id: device_id
            helper_text: 'Device ID'
            helper_text_mode: "persistent"
            size_hint_x: None
            width: dp(200)
        MDRaisedButton:
            id: export_button
            text: 'Export'
            on_release: root.export_node_settings()
            size_hint: (None, None)
            width: dp(100)
            height: dp(40)
            disabled: True
        TextInput:
            id: text_export
            multiline: True
        MDRaisedButton:
            text: 'Back'
            on_release:
                app.screen.ids.sm.current = "main"
                root.manager.transition.direction = "right"
            size_hint_x: 1
            size_hint_y: None
            height: dp(40)

''')
Builder.load_string('''
#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp
#:import App kivy.app.App
#:import os os
#:import RankingsFileChooser orb.screens.rankings.RankingsFileChooser
#:import pref_path orb.misc.utils.pref_path


<RankingsFileChooser>:
    title: 'Import DB'
    size_hint: None, None
    size: min(Window.size[0], dp(800)), min(Window.size[1], dp(800))
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
                width: dp(30)
                size_hint_y: 1
                md_bg_color: 0.3,0.3,0.3,1
                on_release: root.selected_path = filechooser.selection[-1]; root.dismiss()
            MDRaisedButton:
                text: 'Cancel'
                size_hint_x: None
                size_hint_y: 1
                width: dp(30)
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
    size_hint: None, None
    size: min(Window.size[0], dp(800)), min(Window.size[1], dp(800))
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
#:import Window kivy.core.window.Window


<BatchOpenScreen>:
    title: 'Batch Open'
    size: min(Window.size[0], dp(800)), min(Window.size[1], dp(500))
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
                    padding: dp(2)
                    spacing: dp(2)
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
                    MDRaisedButton:
                        text: 'Ingest'
                        on_release: root.ingest(pubkeys.text)
                        size_hint_x: None
                        width: dp(100)
                        height: dp(40)
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
                padding: dp(2)
                spacing: dp(2)
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

<Tab>

''')
Builder.load_string('''
########################################################################################
# NEW ADDRESS
########################################################################################

#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp

<NewAddress>:
    title: "New Wallet Address"
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(500))
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
#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp

<ConnectScreen>:
    name: 'connect'
    title: 'Connect'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(300))
    BoxLayout:
        orientation: 'vertical'
        padding: dp(2)
        spacing: dp(2)
        Splitter:
            horizontal: True
        MDTextField:
            id: address
            helper_text: 'Address'
            helper_text_mode: "persistent"
        Splitter:
            horizontal: True
        MDRaisedButton:
            text: 'Connect'
            height: dp(40)
            size_hint_x: 1
            size_hint_y: None
            on_release: root.connect(address.text)

''')
Builder.load_string('''
#:import Window kivy.core.window.Window

<OpenChannelScreen>:
    title: 'Open Channel'
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(300))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        GridLayout:
            cols: 1
            row_force_default: True
            row_default_height: dp(60)
            padding: dp(2)
            spacing: dp(2)
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
        Widget:
        MDRaisedButton:
            text: 'open'
            on_release: root.open_channel(pk.text, sats.text, sats_per_vbyte.text)
            size_hint: None, None
            width: dp(80)
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
#:import Window kivy.core.window.Window

<Rebalance>:
    title: 'Rebalance'
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(500))
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
            text: '10_000'
            helper_text: 'Max Paths'
            helper_text_mode: "persistent"
        Slider:
            id: time_pref
            value: 0
            min: -1
            max: 1
            step: 0.01
            orientation: 'horizontal'
        Label:
            text: 'Time Preference'
        Label:
            text: "First Hop Channel"
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: dp(30)
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
            height: dp(30)
            size_hint_y: 0
            size_hint_x: 1
            on_text: root.first_hop_spinner_click(spinner_out_id.text)
        Label:
            text: "Last Hop Pubkey"
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: dp(30)
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
            height: dp(30)
            size_hint_y: 0
            size_hint_x: 1
            on_text: root.last_hop_spinner_click(spinner_in_id.text)
        Splitter:
            horizontal: True
        MDRaisedButton:
            text: 'Rebalance'
            font_size: '12sp'
            on_release: root.rebalance() 
            size_hint: 1, None
            height: dp(40)

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import App kivy.app.App
#:import desktop orb.misc.utils.desktop
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
    # disabled: False if desktop else True
    multiline: True
    # size_hint_y: 1 if desktop else 0
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
        on_release: root.se_release()
    StatusLineOutput:
        id: line_output

''')
Builder.load_string('''
<OrbConnector>:
    orientation: 'vertical'
    ScreenManager:
        id: sm
        OrbConnectorMain:
        UmbrelNode:
        VoltageNode:
        ConnectionWizard:
        ConnectionSettings:
        ExportConnectionSettings:
        ImportConnectionSettings:
        ConsoleScreen:
    StatusLine
        id: status_line
''')
Builder.load_string('''
<OrbConnectorMain>:
    name: "main"
    FitImage:
        source: "images/bg.jpeg"
        opacity: 0.1
    GridLayout:
        id: grid
        cols:1
        Splitter:
            horizontal: True
            height: dp(5)
            size_hint_y: 1
        Label:
            text: 'The Lightning Network'
            multiline: True
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: self.texture_size[1]
        Label:
            text: 'just got way more fun!'
            multiline: True
            font_name: 'DejaVuSans'
            font_size: '24sp'
            size_hint_y: None
            height: self.texture_size[1]
        Splitter:
            horizontal: True
            height: dp(5)
            size_hint_y: 1
    MDFloatingActionButtonSpeedDial:
        data: app.data
        root_button_anim: True
        callback: root.add_released
        icon: 'orbit'
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import pref orb.misc.utils.pref
#:import Window kivy.core.window.Window
#:import Clipboard kivy.core.clipboard.Clipboard
#:import Factory kivy.factory.Factory
#:import device_id orb.misc.device_id.device_id

<Tab>

<TypeSpinnerOption@SpinnerOption>:
    size_hint: None, None
    size: dp(150), dp(25)


<ConnectionSettings>:
    name: 'connection_settings'
    BoxLayout:
        orientation: 'vertical'
        MDTabs:
            id: tabs
            Tab:
                title: 'Type & Address'
                BoxLayout:
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Specify the type of node. Set as default, or Umbrel.'
                        size_hint_y: 1
                        multiline: True
                    Spinner:
                        id: spinner_in_id
                        option_cls: Factory.get("TypeSpinnerOption")
                        height: dp(30)
                        width: dp(150)
                        text: 'default'
                        values: ["default", "umbrel"]
                        size_hint: None, None
                        on_text: root.set_and_save('host.type', spinner_in_id.text)
                    MDLabel:
                        text: 'Enter the IP address or hostname of your LND node.'
                        size_hint_y: 1
                        multiline: True
                    BoxLayout:
                        orientation: 'horizontal'
                        height: dp(60)
                        size_hint_y: None
                        MDTextField:
                            id: address
                            # text: pref('host.hostname')
                            helper_text: 'Host Address'
                            helper_text_mode: "persistent"
                            height: dp(60)
                            width: dp(200)
                            size_hint: (None, None)
                        MDRaisedButton:
                            text: 'Save'
                            on_release: root.set_and_save('host.hostname', address.text)
                            size_hint_x: None
                            width: dp(100)
                            height: dp(40)
                            
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
                                # active: pref('lnd.protocol') == 'rest'
                            MDLabel:
                                text: 'REST'
                        BoxLayout:
                            orientation: 'vertical'
                            MDSwitch:
                                id: grpc
                                on_release: root.save_protocol('grpc')
                                # active: pref('lnd.protocol') == 'grpc'
                            MDLabel:
                                text: 'GRPC'
                        BoxLayout:
                            orientation: 'vertical'
                            MDSwitch:
                                id: mock
                                on_release: root.save_protocol('mock')
                                # active: pref('lnd.protocol') == 'mock'
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
                            text: '8080'
                            helper_text: 'REST Port #'
                            helper_text_mode: "persistent"
                            height: dp(60)
                            width: dp(200)
                            size_hint: (None, None)
                        MDTextField:
                            id: grpc_port
                            text: '10009'
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
                        size_hint_y: None
                        height: self.texture_size[1]
                        multiline: True
                    MDIconButton:
                        icon: "content-copy"
                        on_release: root.copy_cert_encrypt_command()
                    TextInput:
                        id: tls_cert
                        text: 
                        on_text: root.validate_cert(self.text)
                        multiline: True
                    MDLabel:
                        id: feedback
                        text: ""
                        multiline: True
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDRaisedButton:
                        text: 'Save'
                        on_release: root.save_cert(tls_cert.text)
                        size_hint: (None, None)
                        width: dp(100)
                        height: dp(40)
                        
                    MDLabel:
                        text: 'Once saved, you can proceed onto the next tab.'
                        size_hint_y: None
                        height: self.texture_size[1]
            Tab:
                title: 'Macaroon'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: (1, 1)
                    MDLabel:
                        text: "Install the 'rsa' module on your node (if you haven't already) with pip3 install rsa then copy and run the provided command on your node."
                        multiline: True
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDIconButton:
                        icon: "content-copy"
                        on_release: root.copy_mac_encrypt_command()
                    TextInput:
                        id: macaroon
                        on_text: root.validate_macaroon(self.text)
                        multiline: True
                    MDLabel:
                        id: mac_feedback
                        text: ""
                        size_hint_y: None
                        height: self.texture_size[1]
                        multiline: True
                    MDRaisedButton:
                        text: 'Save'
                        on_release: root.save_macaroon(macaroon.text)
                        size_hint: (None, None)
                        width: dp(100)
                        height: dp(40)
            Tab:
                title: 'Connect'
                id: connect
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: (1, 1)
                    Widget:
                    MDRaisedButton:
                        text: 'Connect'
                        on_release: root.connect()
                        size_hint: (None, None)
                        width: dp(100)
                        height: dp(40)
                    Widget:

        MDRaisedButton:
            text: 'Back'
            on_release:
                app.screen.ids.sm.current = "main"
                root.manager.transition.direction = "right"
            size_hint_x: 1
            size_hint_y: None
            height: dp(40)

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
#:import Window kivy.core.window.Window
#:import PayInvoicesDialog orb.dialogs.pay_dialogs.pay_invoices_dialog.PayInvoicesDialog
#:import IngestInvoices orb.dialogs.ingest_invoices.ingest_invoices.IngestInvoices

<SpinnerOption>:
    size_hint: None, None
    size: dp(400), dp(25)

<DeezySwapDialog>:
    title: 'Deezy Swap'
    size: min(Window.size[0], dp(400)), min(Window.size[1], dp(300))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            horizontal: True
        MDTextField:
            id: amount_sats
            text: '100_000'
            helper_text: 'Sat Amount'
            helper_text_mode: "persistent"
            on_text: root.estimate_cost(amount_sats.text)
        MDTextField:
            id: cost_estimate
            text: '10_000'
            helper_text: 'Cost Estimate'
            helper_text_mode: "persistent"
        MDRaisedButton:
            id: generate_invoice
            text: 'Generate Invoice'
            font_size: '12sp'
            on_release: root.generate_invoice() 
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)
        Splitter:
            horizontal: True
            size_hint_y: None
            height: dp(5)
        MDRaisedButton:
            id: view_invoices
            text: 'View Invoices'
            font_size: '12sp'
            on_release: IngestInvoices().open()
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)
        Splitter:
            horizontal: True
            size_hint_y: None
            height: dp(5)
        MDRaisedButton:
            id: open_pay
            text: 'Open Pay Dialog'
            font_size: '12sp'
            on_release: PayInvoicesDialog().open()
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import os os
#:import Factory kivy.factory.Factory

<NetworkSpinnerOption@SpinnerOption>:
    size_hint: None, None
    size: dp(200), dp(25)

<VoltageNode>:
    name: 'voltage_node'
    ScrollView:
        size_hint: None, None
        width: root.width
        height: root.height - dp(100)
        pos_hint: {'center_x': .5, 'center_y': .5}
        pos: 0, 0
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            Image:
                source: 'orb/images/voltage.png'
                size: [103, 101]
                size_hint: None, None
            MDTextField:
                id: address
                helper_text: 'Host Address'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(300)
                size_hint: (None, None)
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(10)
            Spinner:
                id: network
                text: 'mainnet'
                option_cls: Factory.get("NetworkSpinnerOption")
                height: dp(25)
                width: dp(200)
                size_hint_y: None
                size_hint_x: None
                values: ["mainnet", "testnet", "signet"]
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(15)
            MDLabel:
                text: 'Admin Macaroon (hex):'
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(5)
            TextInput:
                id: tls_cert
                height: dp(200)
                width: root.width - dp(40)
                size_hint: None, None
                on_text: root.validate_cert(self.text)
                multiline: True
            MDRaisedButton:
                id: connect
                text: 'Connect'
                on_release: root.connect()
                size_hint_x: 1
                height: dp(40)
            MDRaisedButton:
                text: 'Back'
                on_release:
                    app.screen.ids.sm.current = "main"
                    root.manager.transition.direction = "right"
                size_hint_x: 1
                size_hint_y: None
                height: dp(40)

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
########################################################################################
# INGEST INVOICES
########################################################################################

#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp

<IngestInvoices>:
    size_hint: None, None
    size: min(Window.size[0], dp(1000)), min(Window.size[1], dp(800))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    count: count
    title: 'Ingest Invoices'
    BoxLayout:
        padding: dp(2)
        spacing: dp(2)
        orientation: 'vertical'
        GridLayout:
            cols: 1
            padding: dp(2)
            spacing: dp(2)
            TextInput:
                id: invoices
                multiline: True
                size_hint_y: None
                height: dp(150)
            Label:
                id: count
                size_hint_y: None
                height: dp(50)
                text: ''
            ScrollView:
                size_hint: 0.5, 1
                pos_hint: {'center_x': .5, 'center_y': .5}
                do_scroll_x: False
                GridLayout:
                    id: scroll_view
                    cols: 1
                    padding: dp(2)
                    spacing: dp(2)
                    size_hint_y: None
                    height: self.minimum_height
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                padding: dp(2)
                spacing: dp(2)
                height: dp(80)
                MDRaisedButton:
                    id: ingest_button
                    text: 'ingest'
                    size_hint_y: None
                    height: dp(80)
                    width: dp(200)
                    on_release: root.do_ingest(invoices.text)
                MDRaisedButton:
                    id: ingest_button
                    text: 'close'
                    size_hint_y: None
                    height: dp(80)
                    width: dp(200)
                    on_release: root.dismiss()

''')
Builder.load_string('''
########################################################################################
# INVOICE
########################################################################################

#:import datetime datetime.datetime
#:import dp kivy.metrics.dp


<Invoice>
    orientation: 'vertical'
    size_hint_y: None
    height: dp(160)
    padding: dp(2)
    spacing: dp(2)
    canvas.before:
        Color:
            rgba: 55 / 255, 55 / 255, 55 / 255, 0.5
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: dp(40)
        Label:
            text: 'Raw: '
            height: dp(40)
            width: dp(100)
            size_hint_y: None
            size_hint_x: None
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            size_hint_y: None
            height: dp(40)
            text: root.destination[:10] + '...'
            halign: "left"
            valign: "middle"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: dp(40)
        Label:
            text: 'Amount: '
            height: dp(40)
            width: dp(100)
            size_hint_y: None
            size_hint_x: None
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            size_hint_y: None
            height: dp(40)
            text: f'S{int(root.num_satoshis):,}'
            halign: "left"
            valign: "middle"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: dp(40)
        Label:
            text: 'Expires in: '
            height: dp(40)
            width: dp(100)
            size_hint_y: None
            size_hint_x: None
            valign: "middle"
            halign: "left"
            text_size: self.size
        Label:
            id: expiry_label
            size_hint_y: None
            height: dp(40)
            valign: "middle"
            halign: "left"
            text_size: self.size
    BoxLayout:
        orientation: 'horizontal'
        height: dp(40)
        Label:
            text: 'Description: '
            height: dp(40)
            width: dp(100)
            size_hint_y: None
            size_hint_x: None
            valign: "middle"
            halign: "left"
            text_size: self.size
        Label:
            size_hint_y: None
            height: dp(40)
            text: root.description[:50]
            valign: "middle"
            halign: "left"
            text_size: self.size


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
#:import Window kivy.core.window.Window
#:import dp kivy.metrics.dp

<HighlighterDialog>:
    title: 'HighlighterDialog'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    size: min(Window.size[0], dp(500)), min(Window.size[1], dp(150))
    MDTextField:
        id: text_input
        on_text_validate: root.validate(self.text)
        multiline: False

''')
Builder.load_string('''
#: import dp kivy.metrics.dp

<About>:
    title: 'About'
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: None, None
    size: dp(400), dp(400)
    Label:
        id: label
        size_hint: 1, 1
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import os os
#:import Factory kivy.factory.Factory

<NetworkSpinnerOption@SpinnerOption>:
    size_hint: None, None
    size: dp(200), dp(25)

<UmbrelNode>:
    name: 'umbrel_node'
    ScrollView:
        size_hint: None, None
        width: root.width
        height: root.height - dp(100)
        pos_hint: {'center_x': .5, 'center_y': .5}
        pos: 0, 0
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            # Image:
            #     source: 'orb/images/umbrel.png'
            #     size: [103, 101]
            #     size_hint: None, None
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(5)
            MDLabel:
                text: 'lndconnect URl'
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(5)
            TextInput:
                id: lndurl
                height: dp(200)
                width: root.width
                size_hint: None, None
                multiline: True
            MDRaisedButton:
                id: connect
                text: 'Connect'
                on_release: root.connect()
                size_hint_x: 1
                height: dp(40)
            MDRaisedButton:
                text: 'Back'
                on_release:
                    app.screen.ids.sm.current = "main"
                    root.manager.transition.direction = "right"
                size_hint_x: 1
                height: dp(40)

''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import os os
#:import Window kivy.core.window.Window
#:import Clipboard kivy.core.clipboard.Clipboard
#:import Factory kivy.factory.Factory

<Tab>

<AuthSpinnerOption@SpinnerOption>:
    size_hint: None, None
    size: dp(300), dp(25)

<CertFileChooser>:
    title: 'Load Certificate'
    size_hint: [.7,.7]
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        FileChooserIconView:
            show_hidden: True
            size_hint: [1,1]
            id: filechooser
            path: os.path.expanduser('~')
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            height: dp(30)
            MDRaisedButton:
                text: 'Open'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                on_release: root.selected_path = filechooser.selection[-1]; root.dismiss()
            MDRaisedButton:
                text: 'Cancel'
                size_hint_x: None
                width: 30
                size_hint_y: 1
                on_release: root.dismiss()


<ConnectionWizard>:
    name: 'ssh_wizard'
    BoxLayout:
        orientation: 'vertical'
        MDTabs:
            id: tabs
            size_hint_y: 1
            on_tab_switch: root.on_tab_switch(*args)
            SSHCredentials:
                id: ssh_credentials
            NodeAndFiles:
            LNDConf:
            RestartLND:
                id: restart_lnd
            CopyKeys:
        MDRaisedButton:
            text: 'Back'
            on_release:
                app.screen.ids.sm.current = "main"
                root.manager.transition.direction = "right"
            size_hint_x: 1
            height: dp(40)

''')
Builder.load_string('''
#:import os os

<LNDConf>:
    title: 'lnd.conf'
    ScrollView:
        size_hint: 1, 1
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            MDLabel:
                text: 'lnd.conf needs modifying for outside access.'
                size_hint_y: None
                height: dp(50)
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(10)
            MDRaisedButton:
                text: 'Check lnd.conf'
                on_release: root.check_lnd_conf()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            MDLabel:
                id: report
                text: ''
                multiline: True
                size_hint_y: None
                height: self.texture_size[1]
            FocusTextInput:
                id: input
                size_hint_x: .9
                size_hint_y: None
                height: dp(300)
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(10)
            MDRaisedButton:
                text: 'Back up lnd.conf'
                on_release: root.back_up_lnd_conf()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            MDRaisedButton:
                text: 'Restore back-up'
                on_release: root.restore_backup()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            MDRaisedButton:
                text: 'Modify lnd.conf'
                on_release: root.modify_lnd_conf()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            Widget:
                size_hint_y: 1




''')
Builder.load_string('''
<NodeAndFiles>:
    title: 'Node & Files'
    ScrollView:
        size_hint: None, None
        width: root.width
        height: root.height
        pos_hint: {'center_x': .5, 'center_y': .5}
        # pos: 0, dp(40)
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            MDRaisedButton:
                text: 'Detect Node Type'
                on_release: root.detect_node_type()
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            MDTextField:
                id: node_type
                text: 'default'
                helper_text: 'Node Type'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: network
                text: 'mainnet'
                helper_text: 'Network'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: lnd_directory
                text: ''
                helper_text: 'LND directory'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: conf_path
                text: ''
                helper_text: 'lnd.conf path'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: tls_certificate_path
                text: ''
                helper_text: 'TLS certificate path'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: admin_macaroon_path
                text: ''
                helper_text: 'Admin Macaroon path'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: log_path
                text: ''
                helper_text: 'lnd.log path'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: channel_db_path
                text: ''
                helper_text: 'channel.db path'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: lnd_start_cmd
                text: ''
                helper_text: 'lnd start command'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
            MDTextField:
                id: lnd_stop_cmd
                text: ''
                helper_text: 'lnd stop command'
                helper_text_mode: "persistent"
                height: dp(60)
                width: dp(400)
                size_hint: (None, None)
        
''')
Builder.load_string('''
<SSHCredentials>:
    title: 'SSH Credentials'
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1
        spacing: dp(5)
        padding: dp(5)
        MDLabel:
            text: 'Enter SSH credential details to your node.'
            size_hint_y: None
            height: dp(60)
            multiline: True
        MDTextField:
            id: address
            helper_text: 'Host Address'
            helper_text_mode: "persistent"
            height: dp(60)
            width: dp(200)
            size_hint: (None, None)
        MDTextField:
            id: port
            text: '22'
            helper_text: 'SSH port'
            helper_text_mode: "persistent"
            height: dp(60)
            width: dp(200)
            size_hint: (None, None)
        BoxLayout:
            orientation: 'vertical'
            height: dp(80)
            width: dp(300)
            size_hint_y: None
            size_hint_x: None
            Label:
                text: "Authentication"
                size_hint_y: None
            Spinner:
                id: spinner_id
                text: 'certificate'
                option_cls: Factory.get("AuthSpinnerOption")
                height: dp(25)
                size_hint_y: 0
                size_hint_x: 1
                values: ["password", "certificate"]
                on_text: root.cert_or_pass()
        MDTextField:
            id: username
            text: 'ubuntu'
            helper_text: 'Username'
            helper_text_mode: "persistent"
            height: dp(60)
            width: dp(200)
            size_hint: (None, None)
        BoxLayout:
            orientation: 'vertical'
            id: cert_or_pass
        Widget:
        MDRaisedButton:
            id: test_connection
            text: 'Test Connection'
            on_release: root.test_connection()
            size_hint_x: None
            width: dp(200)
            height: dp(40)

''')
Builder.load_string('''

<RestartLND>:
    title: 'Restart LND'
    ScrollView:
        size_hint: 1, 1
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            MDLabel:
                text: 'LND needs restarting to generate new TLS certs.'
                size_hint_y: None
                height: dp(50)
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(10)
            MDRaisedButton:
                text: 'Restart LND'
                on_release: root.restart_lnd()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
                
            FocusTextInput:
                id: input
                size_hint_x: .9
                size_hint_y: None
                height: dp(300)

''')
Builder.load_string('''

<CopyKeys>:
    title: 'Copy Keys'
    ScrollView:
        size_hint: 1, 1
        pos_hint: {'center_x': .5, 'center_y': .5}
        GridLayout:
            cols: 1
            padding: 10
            spacing: 10
            size_hint: 1, None
            height: self.minimum_height
            do_scroll_x: False
            MDLabel:
                text: 'Copy TLS Cert, Macaroon, and set connection settings for LND API to connect to your node.'
                size_hint_y: None
                height: self.texture_size[1]
                multiline: True
            Splitter:
                horizontal: True
                size_hint_y: None
                height: dp(10)
            MDRaisedButton:
                text: 'Copy keys'
                on_release: root.copy_keys()
                size_hint_y: None
                size_hint_x: None
                width: dp(100)
                height: dp(40)
            MDRaisedButton:
                id: connect
                text: 'Connect'
                on_release: root.connect()
                size_hint_x: 1
                height: dp(40)
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window
#:import PayInvoicesDialog orb.dialogs.pay_dialogs.pay_invoices_dialog.PayInvoicesDialog

<SpinnerOption>:
    size_hint: None, None
    size: dp(450), dp(25)

<PayLNURLDialog>:
    title: 'Pay LNURL'
    size: min(Window.size[0], dp(400)), min(Window.size[1], dp(400))
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    size_hint: [None, None]
    BoxLayout:
        orientation: 'vertical'
        Splitter:
            horizontal: True
        MDTextField:
            id: lnurl
            text: 'LNURLXXXX...'
            helper_text: 'LNUrl'
            helper_text_mode: "persistent"
        MDTextField:
            id: rate_limit
            text: '5'
            helper_text: 'Rate Limitting'
            helper_text_mode: "persistent"
        MDTextField:
            id: sats
            text: '1_000_000'
            helper_text: 'Satoshis'
            helper_text_mode: "persistent"
        MDTextField:
            id: chunks
            text: str(10)
            helper_text: 'Chunks'
            helper_text_mode: "persistent"
        MDTextField:
            id: num_threads
            text: str(3)
            helper_text: 'Threads'
            helper_text_mode: "persistent"
        MDRaisedButton:
            text: 'Start generating invoices'
            font_size: '12sp'
            on_release: root.generate_invoices() 
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)
        Splitter:
            horizontal: True
            size_hint_y: None
            height: dp(5)
        MDRaisedButton:
            id: open_pay
            text: 'Open Pay Dialog'
            font_size: '12sp'
            on_release:
                root.dismiss()
                PayInvoicesDialog().open()
            size_hint_y: None
            size_hint_x: 1
            height: dp(40)
''')
Builder.load_string('''
#:import dp kivy.metrics.dp
#:import Window kivy.core.window.Window

<SpinnerOption>:
    size_hint: None, None
    size: dp(400), dp(25)

<PayInvoicesDialog>:
    title: 'Pay Invoices'
    size: min(Window.size[0], dp(400)), min(Window.size[1], dp(400))
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
            text: '10_000'
            helper_text: 'Max Paths'
            helper_text_mode: "persistent"
        Slider:
            id: time_pref
            value: 0
            min: -1
            max: 1
            step: 0.01
            orientation: 'horizontal'
        Label:
            text: 'Time Preference'
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
#:kivy 2.0.0
#:import sp kivy.metrics.sp
#:import dp kivy.metrics.dp

#:import Lnd orb.lnd.Lnd
#:import MailDialog orb.dialogs.mail_dialog.MailDialog
#:import NewAddress orb.screens.new_address_screen.NewAddress
#:import SendCoins orb.screens.send_coins.SendCoins
#:import IngestInvoices orb.dialogs.ingest_invoices.ingest_invoices.IngestInvoices
#:import PayInvoicesDialog orb.dialogs.pay_dialogs.pay_invoices_dialog.PayInvoicesDialog
#:import DeezySwapDialog orb.dialogs.swap_dialogs.deezy_swap.DeezySwapDialog
#:import PayLNURLDialog orb.dialogs.pay_dialogs.pay_lnurl_dialog.PayLNURLDialog
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
#:import Rankings orb.screens.rankings.Rankings
#:import ConnectionWizard orb.dialogs.connection_wizard.connection_wizard.ConnectionWizard
#:import VoltageNode orb.dialogs.voltage_node.voltage_node.VoltageNode
#:import UmbrelNode orb.dialogs.umbrel_node.umbrel_node.UmbrelNode
#:import ConnectionSettings orb.dialogs.connection_settings.ConnectionSettings
#:import AppStoreDialog orb.dialogs.app_store.AppStoreDialog
#:import LoginDialog orb.dialogs.app_store.LoginDialog
#:import UploadAppDialog orb.dialogs.upload_app.UploadAppDialog
#:import HighlighterDialog orb.dialogs.highlighter_dialog.highlighter_dialog.HighlighterDialog


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
        ConsoleScreen:
            id: console
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
                    ContextMenu:
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
                            text: "Highlighter"
                            on_release: [HighlighterDialog().open(), app_menu.close_all()]
                        ContextMenuTextItem:
                            text: "Sort"
                            ContextMenu:
                                ContextMenuTextItem:
                                    text: "ratio"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'ratio'), channels.channels_widget.update())
                                ContextMenuTextItem:
                                    text: "capacity"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'capacity'), channels.channels_widget.update())
                                ContextMenuTextItem:
                                    text: "total-sent"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'total-sent'), channels.channels_widget.update())
                                ContextMenuTextItem:
                                    text: "total-received"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'total-received'), channels.channels_widget.update())
                                ContextMenuTextItem:
                                    text: "out-ppm"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'out-ppm'), channels.channels_widget.update())
                                ContextMenuTextItem:
                                    text: "alias"
                                    on_release: (app_menu.close_all(), set_string_pref('display.channel_sort_criteria', 'alias'), channels.channels_widget.update())
                ContextMenuTextItem:
                    text: "Pay"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "Pay Invoices"
                            on_release: app_menu.close_all()
                            on_press:  PayInvoicesDialog().open()
                        ContextMenuTextItem:
                            text: "Pay LNURL"
                            on_release: app_menu.close_all()
                            on_press:  PayLNURLDialog().open()
                ContextMenuTextItem:
                    text: "Swap"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "Deezy.io"
                            on_release: app_menu.close_all()
                            on_press: DeezySwapDialog().open()
                ContextMenuTextItem:
                    text: "Rebalance"
                    on_release: app_menu.close_all()
                    on_press:  Rebalance().open()
                ContextMenuTextItem:
                    text: "Mail"
                    on_press:  app_menu.close_all()
                    on_release: MailDialog().open()
                ContextMenuTextItem:
                    text: "Connect"
                    on_press:  ConnectScreen().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Ingest Invoices"
                    on_press: IngestInvoices().open()
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
                ContextMenuDivider
                ContextMenuTextItem:
                    id: app_store_login
                    text: "App Store Login"
                    on_press: LoginDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    id: app_store
                    text: "App Store"
                    on_press: AppStoreDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    id: upload_app
                    text: "Upload App"
                    on_press: UploadAppDialog().open()
                    on_release: app_menu.close_all()
                ContextMenuDivider
                ContextMenuTextItem:
                    text: "Channels"
                    on_release: app_menu.close_all()
                    on_press: app.root.ids.sm.current = 'channels'
                ContextMenuTextItem:
                    text: "Console"
                    on_press:  app.root.ids.sm.current = 'console'
                    on_release: app_menu.close_all()
                ContextMenuTextItem:
                    text: "Connector"
                    on_press:  app.connector()
                    on_release: app_menu.close_all()
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
                    text: "Documentation"
                    on_press: app_menu.close_all()
                    on_release: webbrowser.open('https://lnorb.com/docs')
                ContextMenuTextItem:
                    text: "About"
                    on_press: app_menu.close_all()
                    on_release: About().open()
                ContextMenuTextItem:
                    text: "Release Notes"
                    on_press: app_menu.close_all()
                    on_release: webbrowser.open('https://lnorb.com/release-notes')
                ContextMenuTextItem:
                    text: "Lightning Links"
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
                ContextMenuTextItem:
                    text: "Testnet Faucets"
                    ContextMenu:
                        ContextMenuTextItem:
                            text: "BitcoinFaucet"
                            on_release: webbrowser.open("https://bitcoinfaucet.uo1.net")

''')
Builder.load_string('''
<AFView>:
    title: 'Auto Fees'
    size_hint: .9, .9
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        StackLayout:
            size_hint_y: 0.1 if root.size[0] > dp(450) else 0.2
            MDTextField:
                text: str(root.obj['frequency'])
                helper_text: 'Run Frequency'
                helper_text_mode: "persistent"
                size_hint_x: None
                width: dp(100)
                on_text_validate: root.update_obj('frequency', eval(self.text))
            MDTextField:
                text: str(root.obj['spam_prevention'])
                helper_text: 'Time before next update'
                helper_text_mode: "persistent"
                size_hint_x: None
                width: dp(150)
                on_text_validate: root.update_obj('spam_prevention', eval(self.text))
            MDTextField:
                text: str(root.obj['fee_drop_factor'])
                helper_text: 'Fee drop factor'
                helper_text_mode: "persistent"
                size_hint_x: None
                width: dp(100)
                on_text_validate: root.update_obj('fee_drop_factor', eval(self.text))
            MDTextField:
                text: str(root.obj['fee_bump_factor'])
                helper_text: 'Fee bump factor'
                helper_text_mode: "persistent"
                size_hint_x: None
                width: dp(100)
                on_text_validate: root.update_obj('fee_bump_factor', eval(self.text))
        ScrollView:
            size_hint: 1, (0.9 if root.size[0] > dp(450) else 0.8)
            pos_hint: {'center_x': .5, 'center_y': .5}
            GridLayout:
                id: rules
                cols: 1
                padding: 10
                spacing: 10
                size_hint: 1, None
                height: self.minimum_height
                do_scroll_x: False
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: self.minimum_height
            MDIconButton:
                icon: "check-network-outline"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.add_match_rule()
            MDIconButton:
                icon: "clock-start"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.start()


<MatchView@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    canvas:
        Color:
            rgba: .8, .9, .8, .025
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Rule: Match"
        size_hint_y: None
        height: self.texture_size[1]

    MDTextField:
        text: root.rule.alias
        helper_text: 'Rule Name'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('alias', self.text)

    MDTextField:
        text: str(root.rule.priority)
        helper_text: 'Priority'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('priority', int(self.text))

    MDTextField:
        text: '{}'.format(root.rule.fee_rate)
        helper_text: 'Fee Rate (PPM)'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('fee_rate', self.text)

    MDTextField:
        text: root.rule.all[0]
        helper_text: 'Match rule'
        helper_text_mode: "persistent"
        on_text_validate: root.update_rule('all', [self.text])

    MDIconButton:
        icon: "delete-forever"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: root.parent_view.delete_rule(root.index)

''')
Builder.load_string('''
#: import dp kivy.metrics.dp
#: import webbrowser webbrowser

<ABView>:
    title: ''
    size_hint: .9, .9
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        ActionBar:
            pos_hint: {'top':1}
            ActionView:
                use_separator: False
                ActionGroup:
                    text: 'Help' 
                    mode: 'spinner'
                    ActionButton:
                        text: 'Docs'
                        on_release: webbrowser.open('https://lnorb.com/docs/automated_rebalancing.html')
                ActionPrevious:
                    title: 'Auto Balance'
                    app_icon: ''
                    with_previous: False
        MDTextField:
            id: num_threads
            text: str(root.obj.threads) if root.obj else '0'
            helper_text: 'Number of concurrent rebalances'
            helper_text_mode: "persistent"
            size_hint_x: None
            width: dp(100)
            on_text_validate: root.update_obj('threads', int(self.text))
        # MDTextField:
        #     id: max_budget
        #     text: str(root.obj.max_budget) if root.obj else '0'
        #     helper_text: 'Max rebalance budget ({}% of earnings)'.format(int(float(self.text) * 100))
        #     helper_text_mode: "persistent"
        #     size_hint_x: None
        #     width: dp(100)
        #     on_text_validate: root.update_obj('max_budget', float(self.text))
        ScrollView:
            size_hint: 1, 1
            pos_hint: {'center_x': .5, 'center_y': .5}
            GridLayout:
                id: rules
                cols: 1
                padding: 10
                spacing: 10
                size_hint: 1, None
                height: self.minimum_height
                do_scroll_x: False
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: self.minimum_height
            MDIconButton:
                icon: "check-network-outline"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.add_from_to_rule()
            MDIconButton:
                icon: "close-network-outline"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.add_ignore_rule()
            MDIconButton:
                icon: "clock-start"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.start()


<FromToView@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    canvas:
        Color:
            rgba: .8, .9, .8, .025
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Rule: from - to"
        size_hint_y: None
        height: self.texture_size[1]

    MDTextField:
        text: root.rule.alias
        helper_text: 'Rule Name'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('alias', self.text)

    MDTextField:
        text: str(root.rule.fee_rate)
        helper_text: 'Max Fee Rate (PPM)'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('fee_rate', self.text)

    MDTextField:
        text: str(root.rule.time_pref)
        helper_text: 'Time Preference'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('time_pref', self.text)

    MDTextField:
        text: '{:_}'.format(root.rule.num_sats)
        helper_text: 'Amount (SAT)'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('num_sats', int(self.text))

    MDTextField:
        text: root.rule.from_all[0]
        helper_text: 'From rule'
        helper_text_mode: "persistent"
        on_text_validate: root.update_rule('from_all', [self.text])

    MDTextField:
        text: root.rule.to_all[0] if len(root.rule.to_all) else ''
        helper_text: 'To rule'
        helper_text_mode: "persistent"
        on_text_validate: root.update_rule('to_all', [self.text])

    MDIconButton:
        icon: "delete-forever"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: root.parent_view.delete_rule(root.index)


<IgnoreView@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    canvas:
        Color:
            rgba: .8, .9, .8, .025
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "Rule: Ignore"
        size_hint_y: None
        height: self.texture_size[1]

    MDTextField:
        text: root.rule.alias
        helper_text: 'Rule Name'
        helper_text_mode: "persistent"
        normal_color: app.theme_cls.accent_color
        on_text_validate: root.update_rule('alias', self.text)

    MDTextField:
        text: root.rule.all[0] if len(root.rule.all) else ''
        helper_text: 'rule'
        helper_text_mode: "persistent"
        on_text_validate: root.update_rule('all', [self.text])

    MDIconButton:
        icon: "delete-forever"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: root.parent_view.delete_rule(root.index)


''')
Builder.load_string('''
#: import dp kivy.metrics.dp
#: import webbrowser webbrowser

<UpdateMaxHTLCView>:
    title: 'Update Max HTLC MSat'
    size_hint: None, None
    size: dp(400), dp(300)
    background_color: .6, .6, .8, .9
    overlay_color: 0, 0, 0, 0
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Set to 0 when depleted:"
        MDCheckbox:
            active: root.config['config']['disable_depleted']
            on_active: root.config['config']['disable_depleted'] = str(self.active)
        MDTextField:
            text: root.config['config']['depletion_ratio']
            on_text: root.config['config']['depletion_ratio'] = self.text
            helper_text: 'Depletion Ratio'
            helper_text_mode: 'persistent'
        Spinner:
            id: nodes
            text: "Balanced Ratio"
            height: dp(30)
            width: dp(300)
            size_hint: None, None
            values: ['Balanced Ratio', 'Half Capacity', 'Local Balance']
        Widget:
        MDIconButton:
            icon: "clock-start"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: root.start()

''')
Builder.load_string('''

''')
Builder.load_string('''
#:import pref orb.misc.utils.pref
#:import prefs_col orb.misc.utils.prefs_col


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
            group: 'b'
            rgba: prefs_col("display.node_background_color")
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

<HUDEvaluation>:
    text: root.get_text()
    color: 1,1,1,0.1
    font_size: '40sp'
    size_hint: None, None
    size: self.texture_size
    halign: 'center'

<HUDBanner>:
    size_hint: None, None
    size: self.texture_size

<HUDFeeSummary>:
    id: hud_label
    text: root.hud
    size_hint: [None, None]
    markup: True
    size: [self.texture_size[0]+40, self.texture_size[1]+30]

<HUDSpentFeeSummary>:
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

<HUDSystem>:
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
    size: [dp(200), dp(100)]
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
        font_size: '13sp'
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
    HUDN

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
        HUDSpentFeeSummary
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
        HUDSystem


<HUDSE>:
    anchor_x: 'right'
    anchor_y: 'bottom'
    HUDBTCPrice

<HUDN>:
    anchor_x: 'center'
    anchor_y: 'top'
    # HUDEvaluation
    # HUDBanner
    Widget:
    

''')
Builder.load_string('''
<ChannelsWidget>:
    size_hint: 20, 20
    pos: [-self.width/8, -self.height/8]
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
<SegmentLabel>:
    font_size: '84sp'
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