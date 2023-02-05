/*
* @Author: lnorb.com
* @Date:   2022-02-01 18:49:06
* @Last Modified by:   w
* @Last Modified time: 2022-09-06 06:54:11
*/
const SERVICE_DATA = {
    heading: "Who we are",
    
    description: "Nobody. Everybody. We are Satoshi (apart for you Craig).",
    services_list: [{
            key: 1,
            label: "Top 30 node",
            text: "We built Orb in full yolo mode on a node that ended up in the top 30 (as ranked by terminal). We built Orb for our needs, first and foremost.",
            icon: "pe-7s-diamond"
        },
        {
            key: 2,
            label: "We shift sats",
            text: "Our node shifted over 60 BTC in its first 100 days. Orb + Lightning work.",
            icon: "pe-7s-display2"
        },
        {
            key: 3,
            label: "Built in the Plebnet",
            text: "Without the sustained support and knowledge of the plebnet Orb would not exist.",
            icon: "pe-7s-network"
        },
        {
            key: 4,
            label: "Bulk Invoice Management",
            text: "Lightning is all about payments, so Orb enables you to bulk ingest unlimited invoices.",
            icon: "pe-7s-science"
        },
        {
            key: 5,
            label: "Bulk Payments",
            text: "Bulk pay your invoices concurrently. Orb supports shifting vast amounts fast.",
            icon: "pe-7s-news-paper"
        },
        {
            key: 6,
            label: "Easy to customize",
            text: "Orb is deeply configurable, to tweak it to your exact personal preferences.",
            icon: "pe-7s-plane"
        },
        {
            key: 7,
            label: "Multi-touch",
            text: "The Lightning Network has to be experienced. Orb's phone and tablet interface support multi-touch: pinch-zoom, pan, adjust fee-widgets, swipe to rebalance.",
            icon: "pe-7s-arc"
        },
        {
            key: 8,
            label: "Vital Stats",
            text: "How much are channels actually earning? Where are my sats the most valuable? Orb brings the information you want to the forefront of its interface.",
            icon: "pe-7s-study"
        },
        {
            key: 9,
            label: "Programmability",
            text: "Orb is built with devs in mind. Write and publish your solutions to the rest of the network in the same afternoon.",
            icon: "pe-7s-timer"
        },
        {
            key: 7,
            label: "Automated Fees",
            text: "Setting fees is hard - Orb learns what fees route best, and automatically sets your fees for optimal routing and earnings.",
            icon: "pe-7s-cash"
        },
        {
            key: 8,
            label: "Automated Reblancing",
            text: "Rebalancing is time-consuming. Orb keeps your node balanced by shifting sats where they are the most needed",
            icon: "pe-7s-tools"
        },
        {
            key: 8,
            label: "Channel PnL",
            text: "Orb tracks wherher your rebalance bets are winning by tracking their profits and tweaking fees. No more reckless rebalancing.",
            icon: "pe-7s-piggy"
        },
    ]
};

const GALLERY_DATA = {
    heading: '"It\'s beautiful"',
    description: "... is our most common user feedback. Don't believe our users? See for yourself.",
    gallery_list: [
        {
            key: 4,
            label: "We shift sats",
            text: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.49.jpeg",
            thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.49_thumbnail.jpeg",
        },
        {
            key: 4,
            label: "We shift sats",
            text: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.38.jpeg",
            thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.38_thumbnail.jpeg",
        },
        {
            key: 2,
            label: "We shift sats",
            text: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.46.jpeg",
            thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.46_thumbnail.jpeg",
        },
        // {
        //     key: 3,
        //     label: "We shift sats",
        //     text: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.46.jpeg",
        // },
        {
            key: 5,
            label: "We shift sats",
            text: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.51.jpeg",
            thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/photo_2022-03-29 07.25.51_thumbnail.jpeg",
        },
        {
            key: 6,
            label: "We shift sats",
            text: "https://lnorb.s3.us-east-2.amazonaws.com/images/orb-android0.jpeg",
            thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/orb-android0_thumbnail.jpeg",
        },
        // {
        //     key: 6,
        //     label: "We shift sats",
        //     text: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.29.jpg",
        //     thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.29_thumbnail.jpg",
        // },
        // {
        //     key: 7,
        //     label: "We shift sats",
        //     text: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.37.jpg",
        //     thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.37_thumbnail.jpg",
        // },
        // {
        //     key: 8,
        //     label: "We shift sats",
        //     text: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.41.jpg",
        //     thumbnail: "https://lnorb.s3.us-east-2.amazonaws.com/images/2022-04-04 06.34.41_thumbnail.jpg",
        // }
    ]
};

const FEATURES_DATA = {
    title: 'A digital web design studio creating modern & engaging online',
    text: 'Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean.',
    feature_list: [
        'We put a lot of effort in design.',
        'The most important ingredient of successful website.',
        'Submit Your Orgnization.'
    ]
};

const WEBSITE_DESCRIPTION = {
    title: 'Build your dream website today',
    text: 'But nothing the copy said could convince her and so it didn’t take long until a few insidious Copy Writers ambushed her.',
    buttontext: 'View Plan & Pricing'
};

const PRICING_DATA = {
    title: 'Our Pricing',
    description: 'We have a price that fits your profile and your needs.',
    pricing_list: [
        {
            title: 'Free',
            duration: 'Free Forever',
            price: '丰0',
            mobile: 'Yes',
            desktop: 'No',
            auto_rebalancing: 'Yes',
            auto_fees: 'Yes',
            peer_recommendations: 'No',
            bulk_payments: 'No',
            fee_profiles: 'No',
            ads: 'Yes',
            app_store: 'Restricted',
            script_editor: 'No',
            action: 'Coming Soon',
            disabled: true,
            url: 'https://www.apple.com/us/app-store/'
        },
        {
            title: 'Digital Gold',
            duration: '1 Year License',
            price: '丰65K',
            mobile: 'Soon',
            desktop: 'Yes',
            auto_rebalancing: 'Yes',
            auto_fees: 'Yes',
            peer_recommendations: 'Yes',
            bulk_payments: 'No',
            fee_profiles: 'Yes',
            ads: 'No',
            app_store: 'Restricted',
            script_editor: 'Yes',
            action: 'Buy',
            eval_action: 'Evaluate',
            url: '/buy?edition=digital-gold',
            disabled: false,
            eval_url: '/evaluate?edition=digital-gold'
        },
        {
            title: 'Satoshi',
            duration: '1 Year License',
            price: '丰80K',
            mobile: 'Soon',
            desktop: 'Yes',
            auto_rebalancing: 'Yes',
            auto_fees: 'Yes',
            peer_recommendations: 'Yes',
            bulk_payments: 'Yes',
            fee_profiles: 'Yes',
            ads: 'No',
            app_store: 'Full',
            script_editor: 'Yes',
            eval_action: 'Evaluate',
            action: 'Buy',
            url: '/buy?edition=satoshi',
            disabled: false,
            eval_url: '/evaluate?edition=satoshi'
        }
    ]
};

const TEAM_DATA = {
        title: 'Behind The People',
        description: 'It is a long established fact that create category leading brand experiences a reader will be distracted by the readable content of a page when looking at its layout.',
        team_list: [
            {
                profile: '/images/team/img-1.jpg',
                name: 'Frank Johnson',
                designation: 'CEO'
            },
            {
                profile: '/images/team/img-2.jpg',
                name: 'Elaine Stclair',
                designation: 'Designer'
            },
            {
                profile: '/images/team/img-3.jpg',
                name: 'Wanda Arthur',
                designation: 'Developer'
            },
            {
                profile: '/images/team/img-4.jpg',
                name: 'Joshua Stemple',
                designation: 'Manager'
            }
        ]
}

const TESATIMONIAL_DATA = {
    title :'What our users are saying',
    description: "Don't believe us? See what our users have to say:",
    testimonial_list: [
        {
            profile: 'images/testimonials/user-2.jpg',
            description: "Orb is a great application, the community is speedy with responses to troubleshooting questions and the documentation is on point. It’s awesome to see routes/payments being made in real time. Definitely recommended for anyone looking to lighten the load of constant channels rebalancing and fee adjustments",
            name: 'BTC>USD',
            text: 'node',
            url: 'https://amboss.space/node/029507caab603bac8cba5c36d2547bfaf5bc5219614c68eeed0eb581d08011262c'
        },
        {
            profile: 'images/testimonials/user-3.jpg',
            description: "Lnorb offers great multiplatform support and extensive customization options via Python scripting & apps. Having participated in the alpha testing the past few months I have confidence the project will continue expanding the tools end-users have for full-node management while providing quick feedback and fixes to user requests.",
            name: 'hellojessica',
            text: 'node',
            url: 'https://amboss.space/node/03f80288f858251aed6f70142fab79dede5427a0ff4b618707bd0a616527a8cec7'
        },
        {
            profile: 'images/testimonials/user-3.jpg',
            description: "If you run a lightning node, you definitely should try lnorb - while it has the essential tools to manage & control your lightning node, it is its visual aspects and concepts(eg. balance ratios) that give you a different lens to view your node from.  Born in Plebnet, no wonder lnorb gets better with continuous feedback from core-node-runners. Highly recommended!",
            name: 'Dunder Struck',
            text: 'node',
            url: 'https://amboss.space/node/03ddeef790967691c9d7e72b0d76209d9716725d89662bed1fd8b321ba5cad3e87'
        },
        {
            profile: 'images/testimonials/user-3.jpg',
            description: "Orb completely replaces the need for any other lightning related app for complete and secure node management, the fact that I have the flexibility to use it across multiple platforms flawlessly and from anywhere anytime makes this a revolutionary product. The UI is simple,  intuitive, and informative and appealing to the user. The potential for lightning node automation has never been so accomplished as with Orb. Its a home run… I highly recommend Orb.",
            name: 'Warpedspace - PLEBNET.org',
            text: 'node',
            url: 'https://amboss.space/node/0311e4ee7e18ebd68b4e1c425da78a5a8af4d5825ece596d9258d152bd962a7e2b'
        }
    ]
}

const GET_STARTED = {
    newtitle: "Let's Get Started",
    newtext: 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.',
    newbuttontext: 'Get Started'
};

const BLOG_DATA = {
    title :'Latest News',
    description: 'Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean class at a euismod mus luctus quam.',
    blog_list:[
        {
            image: 'images/blog/img-1.jpg',
            text: 'UI & UX Design',
            title: 'Doing a cross country road trip',
            subtext: 'She packed her seven versalia, put her initial into the belt and made herself on the way..'
        },
        {
            image: 'images/blog/img-2.jpg',
            text: 'Digital Marketing',
            title: 'New exhibition at our Museum',
            subtext: 'Pityful a rethoric question ran over her cheek, then she continued her way.'
        },
        {
            image: 'images/blog/img-3.jpg',
            text: 'Travelling',
            title: 'Why are so many people..',
            subtext: 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia.'
        }
    ]
}

const MOCK_DATA = {
    SERVICE_DATA,
    FEATURES_DATA,
    GALLERY_DATA,
    GET_STARTED,
    WEBSITE_DESCRIPTION,
    PRICING_DATA,
    TEAM_DATA,
    TESATIMONIAL_DATA,
    BLOG_DATA
}

export default MOCK_DATA;