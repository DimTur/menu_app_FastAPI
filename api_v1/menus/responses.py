from fastapi import status

get_all_menus_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    }
}

post_menu_responses = {
    status.HTTP_409_CONFLICT: {
        "description": "Menu with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Menu with the same title already exists"}
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    },
}

get_menu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Menu with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Menu with this id not found"}}
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    },
}

patch_menu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Menu with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Menu with this id not found"}}
        },
    },
    status.HTTP_409_CONFLICT: {
        "description": "Menu with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Menu with the same title already exists"}
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    },
}

delete_menu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Menu with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Menu with this id not found"}}
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    },
}
