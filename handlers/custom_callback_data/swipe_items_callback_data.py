from aiogram.filters.callback_data import CallbackData


class SwipeItemsCallbackData(CallbackData, prefix="my"):
    marketplace: str
    current_item_id: int
    part_of_query_path_hash: str
    query: str
