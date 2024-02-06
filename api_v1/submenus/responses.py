from fastapi import status

get_all_submenus_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    }
}

post_submenu_responses = {
    status.HTTP_409_CONFLICT: {
        "description": "Submenu with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Submenu with the same title already exists"}
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

get_submenu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Submenu with this id not found",
        "content": {
            "application/json": {
                "example": {"detail": "Submenu with this id not found"}
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

patch_submenu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Submenu with this id not found",
        "content": {
            "application/json": {
                "example": {"detail": "Submenu with this id not found"}
            }
        },
    },
    status.HTTP_409_CONFLICT: {
        "description": "Submenu with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Submenu with the same title already exists"}
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

delete_submenu_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Submenu with this id not found",
        "content": {
            "application/json": {
                "example": {"detail": "Submenu with this id not found"}
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
