#include <sqlitestorage.h>

#include <memory>

int main() {
    auto db1 = std::make_shared<sqlite::SQLiteStorage>(":memory:");
    db1->open();
    return 0;
}
