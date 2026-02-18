# Jazzmin Admin Panel Settings

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Punyo Market Admin",
    
    # Title on the login screen
    "site_header": "Punyo Market",
    
    # Title on the brand
    "site_brand": "Punyo Market",
    
    # Logo to use for your site
    "site_logo": None,
    
    # Welcome text on the login screen
    "welcome_sign": "Punyo Market Admin Paneliga Xush Kelibsiz",
    
    # Copyright on the footer
    "copyright": "Punyo Market",
    
    # The model admin to search from the search bar
    "search_model": "users.UserProfile",
    
    # Field name on user model that contains avatar
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    
    # Links to put along the top menu
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API Docs", "url": "/swagger/", "new_window": True},
        {"model": "users.UserProfile"},
    ],
    
    #############
    # Side Menu #
    #############
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to aut expand the menu
    "navigation_expanded": True,
    
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.UserProfile": "fas fa-user-circle",
        "orders.Order": "fas fa-shopping-cart",
        "chat.ChatMessage": "fas fa-comments",
    },
    
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "users.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
