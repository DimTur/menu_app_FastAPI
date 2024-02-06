from fastapi import status

get_all_dishes_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    }
}

post_dishes_responses = {
    status.HTTP_409_CONFLICT: {
        "description": "Dish with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Dish with the same title already exists"}
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

get_dish_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Dish with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Dish with this id not found"}}
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

patch_dish_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Dish with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Dish with this id not found"}}
        },
    },
    status.HTTP_409_CONFLICT: {
        "description": "Dish with the same title already exists",
        "content": {
            "application/json": {
                "example": {"detail": "Dish with the same title already exists"}
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

delete_dish_by_id_responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Dish with this id not found",
        "content": {
            "application/json": {"example": {"detail": "Dish with this id not found"}}
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
